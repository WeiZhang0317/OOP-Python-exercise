
class Instructor:
    '''This class is to Initialise the
    instructor name,expertise,experience attributes '''
    def __init__(self, name, expertise, years_of_experience):
        self.__name = name
        self.__expertise = expertise
        self.__years_of_experience = years_of_experience
        self.__workshops = []

    def get_name(self):    
        """ Getter for the name attribute."""
        return self.__name    
    
    def set_name(self, name):
        """ Setter for the name attribute.Must be a non-empty string."""
        if isinstance(name, str) and name.strip():
            self.__name = name
        else:
           raise ValueError("Name must be a non-empty string")
               
    def get_expertise(self):    
        """ Getter for the expertise attribute."""
        return self.__expertise

    def set_expertise(self,expertise):
        """ Setter for the expertise attribute."""
        if isinstance(expertise, str) and expertise.strip():
            self.__expertise = expertise
        else:
           raise ValueError("Expertise must be a non-empty string")
    
    def get_years_of_experience(self):
        """ Getter for the years_of_experience attribute."""
        return self.__years_of_experience 
    
    def set_years_of_experience(self,years_of_experience):
        """ Setter for the years_of_experience attribute."""
        if isinstance(years_of_experience, str) and years_of_experience >=0:
           self.__years_of_experience =years_of_experience
        else:
           raise ValueError("Years of experience must be a positive integer")    
    

    def instructor_profile(self):
        ''' Display the instructor's full profile, including name, expertise, and experience. '''
        return (
            "The name of the instructor is: " + self.__name +
            ", the expertise is: " + self.__expertise +
            ", and the years of experience is: " + str(self.__years_of_experience)
        )
    def add_workshop(self,workshop):
        ''' Add workshop to the instructor.''' 
        self.__workshops.append(workshop)

    def display_workshop(self):    
        ''' Display the list of tech workshops added to the instructor.'''        
        return (
            "The list of tech workshops added to " + self.__name +
            " is: " + ", ".join(self.__workshops)
        )
    
    def __str__(self):
        '''Return the instructor's profile.'''
        return self.instructor_profile()
    
# Testing class Instructor:    
# Instructor1=Instructor("Lee","math",10)  
# print(Instructor1.instructor_profile())

# Instructor1.add_workshop("COMP636")
# Instructor1.add_workshop("COMP640")
# print(Instructor1.display_workshop())



class Participant:
    '''This class is to Initialise the
    participant name, registration number, email address attributes'''
    def __init__(self, name, registration_number, email):
        self.__name = name
        self.__registration_number = registration_number
        self.__email = email
        self.__enrolled_workshops = []
        self.__waitlisted_workshops = []
    
    def enroll_workshops(self,workshop):
        '''Workshops that participant enrolled.''' 
        self.__enrolled_workshops.append(workshop)



    

        
# class Workshop:
#     def __init__(self,name,instructor, date fee=1050, maximum_capacity=20):
#         self.__workshop_name=name
#         self.__workshop_instructor=instructor
#         self.__workshop_fee= fee
#         self.__workshop_maximum_capacity=maximum_capacity
#         self.__workshop_date=date
#         self.__enrolled_participants=[]
#         self.__waitlist_participants=[]
#         self.__attended_participants=[]

    
               



