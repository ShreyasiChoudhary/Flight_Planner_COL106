from flight import Flight
def comparator1(flight1, flight2):
    if (flight1.departure_time- flight2.departure_time)>0: 
        return False
    return True

def comparator3(flight1, flight2):
    if (flight1[0] - flight2[0])>0:
        return False
    return True

def comparator4(flight1, flight2):
    if flight1[0] == flight2[0]:
        if (flight1[1] - flight2[1])>0:
            return False
        return True
    else:
        if (flight1[0] -  flight2[0])>0:
            return False
        return True

class Planner:
    def __init__(self, flights):
        """The Planner

        Args:
            flights (List[Flight]): A list of information of all the flights (objects of class Flight)
        """
        self.m=0
        self.flights = flights
        self.m = max(max(flight.start_city, flight.end_city)for flight in self.flights)
        self.plan = Graph(self.m + 1, comparator1)
        for flight in self.flights:
            self.plan.add_flight(flight)
        

    def least_flights_earliest_route(self, start_city, end_city, t1, t2):
        
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying:
        The route has the least number of flights, and within routes with the same number of flights,
        arrives the earliest.
        """
        if start_city == end_city:
            return[]
        Flight_queue = Queue((len(self.flights) +2))
        best_flight =None
        predecessor = [None]*(len(self.flights)+1)

        visited_flights = [0] * (len(self.flights)+2)
        visited_arrival_time = float('inf')
        visited_flight_count= float('inf')

        flights = self.all_flights(start_city)
        for flight in flights:
            if flight.departure_time >= t1 and flight.arrival_time <= t2:
                Flight_queue.enqueue((1, flight.end_city, flight.arrival_time, flight))
                visited_flights[flight.flight_no] = 1
                if flight.end_city == end_city:
                    if (visited_arrival_time>flight.arrival_time):
                        visited_arrival_time = flight.arrival_time
                        best_flight = flight
                        visited_flight_count = 1

        while not Flight_queue.is_empty():
            x = Flight_queue.dequeue()
            if x is None:
                break
            flight_count, city, arrival_time, curr_flight = x

            if city == end_city:

                if (flight_count < visited_flight_count) or (flight_count == visited_flight_count and arrival_time <= visited_arrival_time):
                    best_flight = curr_flight
                    visited_arrival_time = arrival_time
                    visited_flight_count = flight_count
                    visited_flights[flight.flight_no]=1
                continue

            for flight in self.next_flight(curr_flight, t2):
                if visited_flights[flight.flight_no] == 0:
                    new_flight_count = flight_count + 1
                    new_arrival_time = flight.arrival_time
                    predecessor[flight.flight_no]= curr_flight
                    visited_flights[flight.flight_no]=1
                    Flight_queue.enqueue((new_flight_count, flight.end_city, new_arrival_time, flight))
                    if flight.end_city == end_city:

                        if (new_flight_count<visited_flight_count) or (new_flight_count==visited_flight_count and visited_arrival_time>new_arrival_time):
                            visited_flight_count = new_flight_count
                            visited_arrival_time = new_arrival_time
                            best_flight = flight
        route =[]
        curr_flight = best_flight
        while curr_flight is not None:
            route.append(curr_flight)
            curr_flight = predecessor[curr_flight.flight_no]
        return route[::-1]

 
    def cheapest_route(self, start_city, end_city, t1, t2):
        if start_city == end_city:
            return[]
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route is a cheapest route
        """
        best_fare = float('inf')
        visited_flights = [0]*(len(self.flights)+2)
        flights = self.all_flights(start_city)
        init_array =[]
        predecessor = [None]*(len(self.flights)+1)
        best_flight = None
        Flight_heap= Heap(comparator3, init_array)
        for flight in flights:
            if flight.departure_time>= t1 and flight.arrival_time<=t2:
                Flight_heap.insert((flight.fare, flight))
                visited_flights[flight.flight_no] = 1
                if flight.end_city == end_city:
                    if flight.fare<best_fare:
                        best_flight = flight
                        best_fare = flight.fare
        while not Flight_heap.is_empty():
           s = Flight_heap.extract()
           fare = s[0]
           curr_flight = s[1]
           if curr_flight.end_city == end_city and fare<best_fare:
            visited_flights[curr_flight.flight_no] = 1
            best_flight = curr_flight
            best_fare = fare
            continue

           for flight in self.next_flight(curr_flight, t2):
            if visited_flights[flight.flight_no] == 0:
                new_fare = fare + flight.fare
                predecessor[flight.flight_no] = curr_flight
                Flight_heap.insert((new_fare, flight))
                visited_flights[flight.flight_no] = 1
                if flight.end_city == end_city:
                        if best_fare>new_fare:
                            best_flight = flight
                            best_fare = new_fare
        route=[]
        curr_flight = best_flight
        while curr_flight is not None:
            route.append(curr_flight)
            curr_flight = predecessor[curr_flight.flight_no]
        return route[::-1]

    
    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        if start_city == end_city:
            return[]
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        is the cheapest
        """
        visited_fare = float('inf')
        visited_flights = [0]*(len(self.flights)+2)
        visited_flight_count = float('inf')
        flights = self.all_flights(start_city)
        init_array =[]
        predecessor = [None]*(len(self.flights) +1)
        best_flight = None
        Flight_heap= Heap(comparator4, init_array)
        for flight in flights:
            if flight.departure_time>= t1 and flight.arrival_time<=t2:
                Flight_heap.insert((1, flight.fare, flight))
                visited_flights[flight.flight_no] = 1
                if flight.end_city == end_city:
                    if flight.fare<visited_fare:
                        best_flight = flight
                        visited_fare = flight.fare
                        visited_flight_count = 1
        while not Flight_heap.is_empty():
            s = Flight_heap.extract()
            r = s[0]
            fare = s[1]
            curr_flight = s[2]
            if end_city == curr_flight.end_city:
                best_flight = curr_flight
                break
            for flight in self.next_flight(curr_flight, t2):
                if visited_flights[flight.flight_no]==0:
                    new_flight_count = r+1
                    new_fare = fare + flight.fare
                    new_flight_count= r+1
                    predecessor[flight.flight_no]=curr_flight
                    visited_flights[flight.flight_no] = 1
                    Flight_heap.insert((r+1, new_fare, flight))
                    if flight.end_city == end_city:
                        if (visited_flight_count>new_flight_count) or (visited_flight_count==new_flight_count and visited_fare>new_fare):
                            best_flight = flight
                            visited_flight_count = new_flight_count
                            visited_fare = new_fare
        route=[]
        curr_flight = best_flight
        while curr_flight is not None:
            route.append(curr_flight)
            curr_flight = predecessor[curr_flight.flight_no]
        return route[::-1]


    def all_flights(self, start_city):
        return self.plan.list[start_city]
    def next_flight(self, flight, t2):
        new_city = flight.end_city
        arrival_time = flight.arrival_time
        t1 = arrival_time + 20
        available_flights =[]
        for flight in self.all_flights(new_city):
            if flight.departure_time>=t1 and flight.arrival_time<=t2:
                available_flights.append(flight)
        return available_flights

class Graph:
    def __init__(self, n, comparator = comparator1):
        self.comparator = comparator
        self.list = [[] for i in range(n)]
    def add_flight(self, flight):
        self.list[flight.start_city].append(flight)

class Heap:
    '''
    Class to implement a heap with general comparison function
    '''
    
    def __init__(self, comparison_function, init_array):
        self._heap = init_array
        self.comparison_function = comparison_function
        if len(self._heap)>1:
            self.heapify()
        
        '''
        Arguments:
            comparison_function : function : A function that takes in two arguments and returns a boolean value
            init_array : List[Any] : The initial array to be inserted into the heap
        Returns:
            None
        Description:
            Initializes a heap with a comparison function
            Details of Comparison Function:
                The comparison function should take in two arguments and return a boolean value
                If the comparison function returns True, it means that the first argument is to be considered smaller than the second argument
                If the comparison function returns False, it means that the first argument is to be considered greater than or equal to the second argument
        Time Complexity:
            O(n) where n is the number of elements in init_array
        '''
        
        # Write your code here
        
    def insert(self, value):
        self._heap.append(value)
        self.upheap(len(self._heap) - 1)
        '''
        Arguments:
            value : Any : The value to be inserted into the heap
        Returns:
            None
        Description:
            Inserts a value into the heap
        Time Complexity:
            O(log(n)) where n is the number of elements currently in the heap
        '''
        
        # Write your code here
    
    def extract(self):
        if not self.is_empty():
            self.swap(0, (len(self._heap)-1))
            a=self._heap.pop()
            if len(self._heap) != 0:
                self.downheap(0)
            return a
        '''
        Arguments:
            None
        Returns:
            Any : The value extracted from the top of heap
        Description:
            Extracts the value from the top of heap, i.e. removes it from heap
        Time Complexity:
            O(log(n)) where n is the number of elements currently in the heap
        '''
        
        # Write your code here

    
    def top(self):
        '''
        Arguments:
            None
        Returns:
            Any : The value at the top of heap
        Description:
            Returns the value at the top of heap
        Time Complexity:
            O(1)
        '''
        
        # Write your code here
        if not self.is_empty():
            a = self._heap[0]
            return a
        return None
    
    def parent(self, integ):
        return ((integ-1)//2)
    
    def left_child(self, integ):
        if self.has_left(integ):
            return (2*integ +1)
    
    def right_child(self, integ):
        if self.has_right(integ):
            return (2*integ + 2)
            
    def has_left(self, integ):
        if (2*integ + 1) < len(self._heap):
            return True
        else:
            return False
            
    def has_right(self, integ):
        if (2*integ +2) < len(self._heap):
            return True
        else:
            return False
    def swap (self, int1, int2):
        self._heap[int1], self._heap[int2] = self._heap[int2], self._heap[int1]
        
    def downheap (self, integ):
        if self.has_left(integ):
            left_child = self.left_child(integ)
            small_child = left_child
            if self.has_right(integ):
                right_child = self.right_child(integ)
                if self.comparison_function(self._heap[right_child],self._heap[left_child]) is True:
                    small_child = right_child
            if self.comparison_function(self._heap[small_child],self._heap[integ]) is True:
                self.swap(small_child, integ)
                self.downheap(small_child)
                
    def upheap (self, integ):
        parent = self.parent(integ)
        if parent >=0 :
            if self.comparison_function(self._heap[parent],self._heap[integ]) is False:
                self.swap(parent, integ)
                self.upheap(parent)
                
    def heapify(self):
        last = len(self._heap) -1
        for i in range(last, -1, -1):
            self.downheap(i)
            
    def __len__(self):
        return len(self._heap)
        
    def is_empty (self):
        return (len(self._heap)==0)
    
        
class Queue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.init_array = [None] * capacity
        self.front = 0
        self.rear = 0
    
    def len(self):
        return (self.rear - self.front + self.capacity) % self.capacity
    
    def enqueue(self, value):
        if self.len() == self.capacity - 1:  # Only one slot left means full
            self.resize(2 * self.capacity)
        self.init_array[self.rear] = value
        self.rear = (self.rear + 1) % self.capacity
    
    def is_empty(self):
        return self.len() == 0

    def dequeue(self):
        value = None
        if not self.is_empty():
            value = self.init_array[self.front]
            self.init_array[self.front] = None
            self.front = (self.front + 1) % self.capacity
        return value
    
    def top(self):
        if not self.is_empty():
            return self.init_array[self.front]
        else:
            raise IndexError("Queue is empty")
    
    def resize(self, capacity):
        old = self.init_array
        self.init_array = [None] * capacity
        walk = self.front
        for i in range(self.len()):
            self.init_array[i] = old[walk]
            walk = (walk + 1) % self.capacity
        self.rear = self.len()
        self.front = 0
        self.capacity = capacity