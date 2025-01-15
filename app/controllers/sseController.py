"""
Server-Sent Events (SSE) Controller Module

This module handles real-time event streaming to clients using Server-Sent Events.
It maintains a persistent connection with clients and broadcasts book-related operations
in real-time.

Author: [Your Name]
Created: [Date]
"""

import json
import asyncio
import logging
from datetime import datetime
from typing import AsyncGenerator, Dict

from fastapi import Response
from sse_starlette.sse import EventSourceResponse

from app.events.manager import event_manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def stream_updates() -> EventSourceResponse:
    """
    Establishes and manages a Server-Sent Events connection with clients.
    
    Creates a dedicated queue for the client, sends an initial connection message,
    and continuously streams events until the connection is closed.

    Returns:
        EventSourceResponse: SSE response object with continuous event stream

    Notes:
        - The connection remains open until the client disconnects
        - Each client gets their own dedicated queue for events
        - Events are delivered in real-time as they occur
        - The connection automatically handles reconnection attempts
    """
    client_queue = await event_manager.connect()
    logger.info("New SSE client connected")
    
    async def event_generator() -> AsyncGenerator[Dict, None]:
        """
        Generates SSE events for the client stream.

        Yields:
            Dict: Event data containing event type and JSON-formatted payload

        Notes:
            - Sends initial connection confirmation
            - Continuously yields new events from the client queue
            - Properly handles connection cleanup on disconnection
        """
        try:
            # Initial connection event
            initial_event = {
                "event": "bookOperation",
                "data": json.dumps({
                    "timestamp": datetime.now().isoformat(),
                    "type": "connection",
                    "message": "SSE connection established"
                })
            }
            logger.debug("Sending initial connection event")
            yield initial_event
            
            # Main event loop
            while True:
                event = await client_queue.get()
                logger.debug(f"Broadcasting event: {event.get('event')}")
                yield event
                
        except asyncio.CancelledError:
            logger.info("SSE connection cancelled by client")
            raise
        finally:
            logger.info("Cleaning up SSE connection")
            event_manager.disconnect(client_queue)

    # Return SSE response with appropriate headers
    return EventSourceResponse(
        event_generator(),
        headers={
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache, no-transform',
            'Content-Type': 'text/event-stream',
            'X-Accel-Buffering': 'no'
        }
    )
