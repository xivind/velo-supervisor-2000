#!/usr/bin/env python3
"""Scheduler for automated maintenance tasks"""

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from business_logic import BusinessLogic

SCHEDULER = None

def start_scheduler():
    """Initialize and start the APScheduler instance"""
    global SCHEDULER

    try:
        logging.info("Initializing APScheduler...")

        SCHEDULER = AsyncIOScheduler()

        SCHEDULER.add_job(update_time_based_fields_job,
                          trigger=CronTrigger(hour=3, minute=0),
                          id='update_time_based_fields',
                          name='Update component time-based status fields',
                          replace_existing=True,
                          misfire_grace_time=3600)

        SCHEDULER.start()
        logging.info("APScheduler started successfully. Jobs registered:")
        logging.info(" * update_time_based_fields: Daily at 3:00 AM")

    except Exception as exception:
        logging.error(f"Failed to start scheduler: {exception}")
        raise

def stop_scheduler():
    """Gracefully shutdown the APScheduler instance"""
    global SCHEDULER

    if SCHEDULER is not None:
        try:
            logging.info("Shutting down APScheduler...")
            SCHEDULER.shutdown(wait=True)
            logging.info("APScheduler shut down successfully")
        
        except Exception as exception:
            logging.error(f"Error during scheduler shutdown: {exception}")
    
    else:
        logging.debug("Scheduler was not running, no shutdown needed")

async def update_time_based_fields_job():
    """Scheduled job to update time-based status fields for all non-retired components"""
    try:
        logging.info("Starting scheduled job: update_time_based_fields")

        business_logic = BusinessLogic(app_state=None)

        success, message = business_logic.update_time_based_fields()

        if success:
            logging.info(f"Scheduled job completed successfully: {message}")
        
        else:
            logging.error(f"Scheduled job completed with errors: {message}")

    except Exception as exception:
        logging.error(f"Critical error in scheduled job update_time_based_fields: {exception}")
