from datetime import datetime, timezone, timedelta
import aiohttp
from bs4 import BeautifulSoup
import gspread
from gspread import utils
import os
from typing import Dict, List
import pytz

async def fetch_event_description(event_id: str) -> str:
    """Fetch the event description from the CTFtime event page"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://ctftime.org/event/{event_id}') as response:
                if response.status != 200:
                    return ""
                
                content = await response.text()
                soup = BeautifulSoup(content, 'html.parser')
                
                description_div = soup.find('div', {'id': 'id_description'})
                if description_div:
                    description = description_div.get_text(separator='\n', strip=True)
                    return description
                return ""
    except Exception as e:
        print(f"[CTFTime] Error fetching event description: {str(e)}")
        return ""

def parse_ctftime_date(date_str: str) -> datetime:
    """Parse CTFtime date format (YYYYMMDDTHHMMSS) to datetime"""
    return datetime.strptime(date_str, '%Y%m%dT%H%M%S').replace(tzinfo=timezone.utc)

def truncate_description(description: str, max_length: int = 1000, suffix: str = "...") -> str:
    """Truncate description to specified length if needed"""
    if len(description) > max_length:
        return description[:max_length - len(suffix)] + suffix
    return description

def get_gspread_client() -> gspread.Client:
    """Get Google Sheets client from environment credentials"""
    project_id = os.getenv('GOOGLE_PROJECT_ID')
    private_key = os.getenv('GOOGLE_PRIVATE_KEY')
    private_key_id = os.getenv('GOOGLE_PRIVATE_KEY_ID')
    client_email = os.getenv('GOOGLE_CLIENT_EMAIL')
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    
    if not (project_id or private_key or private_key_id or client_email or client_id):
        raise ValueError("Missing Google Sheets credentials")
    
    credentials = {
        "type": "service_account",
        "token_uri": "https://oauth2.googleapis.com/token",
        "project_id": project_id,
        "private_key_id": private_key_id,
        "private_key": private_key,
        "client_email": client_email,
        "client_id": client_id
    }
        
    return gspread.service_account_from_dict(credentials)

def convert_to_est(dt: datetime) -> datetime:
    """Convert UTC datetime to EST"""
    est = pytz.timezone('America/New_York')
    return dt.astimezone(est)

def format_sheet_date(dt: datetime) -> str:
    """Format datetime for Google Sheets (e.g., '7/18/2025')"""
    est_dt = convert_to_est(dt)
    return est_dt.strftime("%-m/%-d/%Y")

def format_sheet_time(dt: datetime) -> str:
    """Format time for Google Sheets (e.g., '11:00:00 PM')"""
    est_dt = convert_to_est(dt)
    return est_dt.strftime("%I:%M:%S %p")

def format_duration(start: datetime, end: datetime) -> str:
    """Format duration for Google Sheets (e.g., '1 days 00:00')"""
    duration = end - start
    days = duration.days
    hours = duration.seconds // 3600
    minutes = (duration.seconds % 3600) // 60
    
    if days > 0:
        return f"{days} days {hours:02d}:{minutes:02d}"
    else:
        return f"0 days {hours:02d}:{minutes:02d}"

def excel_date_to_datetime(excel_date: float, excel_time: float = 0) -> datetime:
    """Convert Excel serial date/time to datetime"""
    # Excel's date system starts from December 30, 1899
    excel_start = datetime(1899, 12, 30, tzinfo=timezone.utc)
    
    # Convert days to timedelta
    days = int(excel_date)
    
    # Convert time fraction to hours, minutes, seconds
    day_seconds = int(excel_time * 24 * 3600)
    hours = day_seconds // 3600
    minutes = (day_seconds % 3600) // 60
    seconds = day_seconds % 60
    
    return excel_start + timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

def parse_sheet_datetime(date_val: any, time_val: any) -> datetime:
    """Parse sheet date and time values to datetime"""
    try:
        # Handle numeric (Excel-style) values
        if isinstance(date_val, (int, float)) and isinstance(time_val, (int, float)):
            return excel_date_to_datetime(date_val, time_val)
            
        # Handle string values (fallback)
        if isinstance(date_val, str) and isinstance(time_val, str):
            try:
                # Try new format (e.g., "5/16/2025", "10:00:00 PM")
                est = pytz.timezone('America/New_York')
                dt = datetime.strptime(f"{date_val} {time_val}", "%-m/%-d/%Y %I:%M:%S %p")
                return est.localize(dt).astimezone(pytz.UTC)
            except ValueError:
                return None
                
        return None
    except Exception as e:
        print(f"[GSheet] Error parsing date/time: {str(e)}")
        return None

async def update_ctf_spreadsheet(events: List[Dict]):
    """Update Google Sheets with CTF events"""
    try:
        # Get Google Sheets client
        gc = get_gspread_client()
        
        # Open the CTF Events spreadsheet
        sheet_url = os.getenv('GOOGLE_SHEETS_URL')
        if not sheet_url:
            raise ValueError("GOOGLE_SHEETS_URL environment variable not set")
            
        sh = gc.open_by_url(sheet_url)
        current_year = datetime.now().year
        worksheet = sh.worksheet(str(current_year)) # e.g. "2025"
        
        # Get raw cell values (not formatted display values)
        data = worksheet.get('A2:G', value_render_option='UNFORMATTED_VALUE')
        print(f"[GSheet] Found {len(data)} existing events in the {current_year} sheet")
        
        # Process existing events to get their timestamps and names
        existing_names = set()
        parsed_events = []
        
        for row in data:
            if len(row) >= 8:  # Only process valid rows
                try:
                    # Store event name for duplicate checking
                    event_name = row[0].strip()
                    existing_names.add(event_name)
                    
                    # Print raw values for debugging
                    print(f"[GSheet] Raw row data: {row}")
                    print(f"[GSheet] Date value: {repr(row[1])}")
                    print(f"[GSheet] Time value: {repr(row[2])}")
                    
                    # Try to parse the date/time
                    start_time = parse_sheet_datetime(row[1], row[2])
                    if start_time:
                        parsed_events.append({
                            'start_time': start_time,
                            'row': list(row),  # Convert to list to ensure mutability
                            'name': event_name
                        })
                        print(f"[GSheet] Successfully parsed existing event: {event_name} on {row[1]} at {row[2]}")
                    else:
                        print(f"[GSheet] Failed to parse date for event: {event_name} with date {row[1]} {row[2]}")
                except Exception as e:
                    print(f"[GSheet] Error processing existing event {row[0]}: {str(e)}")
        
        print(f"[GSheet] Successfully parsed {len(parsed_events)} existing events in the {current_year} sheet")
        
        # Process new events
        new_events = []
        for event in events:
            start_time = parse_ctftime_date(event['start_date'])
            
            # Skip if event is in next year
            if start_time.year > current_year:
                print(f"[GSheet] Skipping event {event['title']} - it's for {start_time.year}")
                continue
                
            event_name = event['title'].strip()
            
            # Skip if name already exists
            if event_name in existing_names:
                print(f"[GSheet] Skipping duplicate event: {event_name}")
                continue
                
            end_time = parse_ctftime_date(event['end_date'])
            
            row = [
                event_name,                             # Event Name
                format_sheet_date(start_time),          # Start Date
                format_sheet_time(start_time),          # Start Time
                format_sheet_date(end_time),            # End Date
                format_sheet_time(end_time),            # End Time
                format_duration(start_time, end_time),  # Duration
                event['weight'],                        # Weight
                f"https://ctftime.org{event['ctftime_url']}",  # Link
                # Cells for availability (20 max for now, can increase later)
                "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
            ]
            
            new_events.append({
                'start_time': start_time,
                'row': row,
                'name': event_name
            })
            print(f"[GSheet] Processing new event: {event_name} on {row[1]} at {row[2]}")
        
        if not new_events:
            print("[GSheet] No new events to add")
            return
            
        # Sort all events by start time
        all_events = parsed_events + new_events
        all_events.sort(key=lambda x: x['start_time'])
        
        # Create the final list of rows
        final_rows = [event['row'] for event in all_events]
        
        print(f"[GSheet] Updating sheet with {len(final_rows)} total events ({len(new_events)} new)")
        
        # Set up dropdown validation for availability columns
        worksheet.add_validation(
            'H2:AA1000',
            utils.ValidationConditionType.one_of_list,
            ['Yes', 'Yes?', 'No?', 'No'],
            showCustomUi=True
        )
        
        # Update entire sheet at once, preserving raw values
        worksheet.update('A2', final_rows, raw=False)
        
        # Log what happened
        print(f"[GSheet] Added {len(new_events)} new events")
        for event in new_events:
            print(f"[GSheet] Added: {event['name']} starting at {event['start_time']}")
        
    except Exception as e:
        print(f"[GSheet] Error updating spreadsheet: {str(e)}") 