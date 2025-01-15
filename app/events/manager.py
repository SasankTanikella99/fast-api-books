"""
Server-Sent Events Manager Module

This module implements a real-time event broadcasting system using Server-Sent Events (SSE).
It manages client connections and handles event broadcasting for book-related operations.

Author: Sasank Tanikella
Created: 01-14-2025
"""

from datetime import datetime, date
import json
from typing import List, Dict, Optional, Any
import asyncio

class DateTimeEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for datetime objects.
    
    Extends the standard JSON encoder to properly serialize datetime
    and date objects to ISO format strings.
    """
    def default(self, obj: Any) -> str:
        """
        Convert datetime/date objects to ISO format strings.

        Args:
            obj: Object to be serialized

        Returns:
            str: ISO formatted string for datetime/date objects
            Any: Default serialization for other types
        """
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(obj)

class SSEManager:
    """
    Server-Sent Events manager for handling real-time updates.
    
    Manages client connections and broadcasts events to all connected clients.
    Implements connection handling and event broadcasting with proper serialization.
    """

    def __init__(self):
        """Initialize the SSE manager with an empty client list."""
        self._clients: List[asyncio.Queue] = []
        
    async def connect(self) -> asyncio.Queue:
        """
        Establish a new client connection.

        Creates a new queue for the client and adds it to the client list.

        Returns:
            asyncio.Queue: Dedicated queue for the new client

        Notes:
            - Each client gets its own asyncio Queue
            - Queue is used for sending events to the specific client
        """
        queue = asyncio.Queue()
        self._clients.append(queue)
        return queue
    
    def disconnect(self, queue: asyncio.Queue) -> None:
        """
        Remove a client connection.

        Args:
            queue: Client's queue to be removed

        Notes:
            - Safely removes client's queue from the client list
            - Called when client disconnects or connection errors occur
        """
        if queue in self._clients:
            self._clients.remove(queue)
    
    def serialize_book_data(self, book_data: Optional[Dict]) -> Optional[Dict]:
        """
        Serialize book data for JSON transmission.

        Converts datetime/date objects to ISO format strings and handles
        other serialization requirements.

        Args:
            book_data: Dictionary containing book information

        Returns:
            Optional[Dict]: Serialized book data or None if input is None

        Notes:
            - Handles datetime/date serialization
            - Preserves original data structure
            - Returns None for empty input
        """
        if book_data:
            serialized_data = {}
            for key, value in book_data.items():
                if isinstance(value, (date, datetime)):
                    serialized_data[key] = value.isoformat()
                else:
                    serialized_data[key] = value
            return serialized_data
        return None
            
    async def broadcast(
        self, 
        event_type: str, 
        message: str, 
        book_id: Optional[int] = None, 
        book_data: Optional[Dict] = None
    ) -> None:
        """
        Broadcast an event to all connected clients.

        Args:
            event_type: Type of event (e.g., 'bookCreated', 'bookUpdated')
            message: Event description message
            book_id: Optional ID of the affected book
            book_data: Optional dictionary containing book details

        Notes:
            - Broadcasts to all connected clients
            - Handles data serialization
            - Includes timestamp with each event
            - Skips if no clients are connected
            
        Example:
            >>> await event_manager.broadcast(
                    "bookCreated",
                    "New book added",
                    book_id=1,
                    book_data={"title": "Example Book"}
                )
        """
        if not self._clients:
            return
            
        serialized_book_data = self.serialize_book_data(book_data)
            
        event = {
            "event": "bookOperation",
            "data": json.dumps({
                "timestamp": datetime.now().isoformat(),
                "type": event_type,
                "message": message,
                "book_id": book_id,
                "book_data": serialized_book_data
            }, cls=DateTimeEncoder)
        }
        
        for queue in self._clients:
            await queue.put(event)

# Global instance of SSE manager
event_manager = SSEManager()
