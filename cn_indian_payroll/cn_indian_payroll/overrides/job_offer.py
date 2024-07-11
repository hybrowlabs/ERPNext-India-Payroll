import frappe

def on_update_after_submit(doc,method):
    from nextai.funnel.custom_trigger import trigger_event
    trigger_event(doc=doc, event_name="update_on_submit")