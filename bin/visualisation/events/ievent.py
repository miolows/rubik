from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import Sequence
# from panda3d.core import *


def handle_event(event:str):
    '''
    A decoratoring function that allows to mark methods to be an event handlers 
    for a given message.
    
    Parameters
    ----------
    event : str - Message of an event.
    '''
    def inner_event(func):
        func.event_name = event
        return func
    return inner_event

class IEventOrganiser(DirectObject):
    def __init__(self):
        '''
        It iterates over all member methods, looking for this attribute and 
        automatically accepts for the given event name and handler method.
        '''
        for attrib in dir(self):
            method = getattr(self, attrib)
            if callable(method) and hasattr(method, 'event_name'):
                self.accept(method.event_name, method)

    def destroy(self):
        self.ignoreAll()
        
        
def event_sender(event_msg, *args):
    messenger.send(event_msg, sentArgs=[*args])