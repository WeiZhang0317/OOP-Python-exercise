
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
        return self.__name   

    def instructor_profile(self):
        ''' Display the instructor's full profile, including name, expertise, and experience. '''
        return (
            "The name of the instructor is: " + self.__name +
            ", the expertise is: " + self.__expertise +
            ", and the years of experience is: " + str(self.__years_of_experience)
        )
    def assign_workshop(self,workshop):
        ''' assign workshop to the instructor.''' 
        self.__workshops.append(workshop)

    def display_workshop(self):    
        ''' Display the list of tech workshops assigned to the instructor.'''        
        return (
            "The list of tech workshops assigned to " + self.__name +
            " is: " + ", ".join(self.__workshops)
        )
Instructor1=Instructor("Lee","math",10)  
print(Instructor1.instructor_profile())

Instructor1.assign_workshop("COMP636")
Instructor1.assign_workshop("COMP640")
print(Instructor1.display_workshop())







# class Participant:
#     def __init__(self, name, registration_number, email):
#         self.__name = name
#         self.__registration_number = registration_number
#         self.__email = email
#         self.__enrolled_workshops = []
#         self.__waitlisted_workshops = []

        
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

    
               



