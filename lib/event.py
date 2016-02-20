import threading

class Event:
    event_counter = 0
    def checkDictExists(self):
        '''
        Method that checks if the array self.__listeners already exists, and
        initializes it empty otherwise
        '''
        try:
            self.__listeners
        except:
            self.__listeners = {}

    def checkArrayExists(self, key):
        try:
            self.__listeners[key]
        except:
            self.__listeners[key] = []

    def on(self, event, target, priority=20):
        self.event_counter += 1
        self.checkDictExists()
        self.checkArrayExists(event)
        newListener = {'id': self.event_counter,'target':target, 'priority':priority}
        if len(self.__listeners[event]) == 0:
            self.__listeners[event].append(newListener)
        elif self.__listeners[event][0]['priority'] > newListener['priority']:
            self.__listeners[event].insert(0, newListener)
        else:
            for key, listener in enumerate(self.__listeners[event]):
                try:
                    nextListener = self.__listeners[event][key+1]
                    if nextListener['priority'] > newListener['priority']:
                        self.__listeners[event].insert(key+1, newListener)
                        break
                except IndexError:
                    self.__listeners[event].append(newListener)
                    break

    def removeListener(self, listenerID):
        for event in self.__listeners:
            for index, listener in enumerate(self.__listeners[event]):
                if listener['id'] == listenerID:
                     del self.__listeners[event][index]
                     break



    def event(self, event, caller, data=None):
        threading.Thread(target=self.eventCalled, kwargs={'event':event, 'caller':caller, 'data':data}).start()

    def eventCalled(self, event, caller, data=None):
        self.checkDictExists()
        self.checkArrayExists(event)
        for listener in self.__listeners[event]:
            if not data==None:
                listener['target'](caller, data)
            else:
                listener['target'](caller)
