# Attributes
# − The name of the tech workshop. 
# − The instructor assigned to conduct the workshop (an object of the Instructor 
# class). 
# − The fee amount for the workshop ($1050). 
# − The maximum capacity of the workshop (20). 
# − The date of the workshop. 
# − A list of participants (objects of the Participant class) enrolled in the workshop. 
# − A list of participants (objects of the Participant class) who are on the waitlist for 
# the workshop. 
# − A list of participants (objects of the Participant class) who attended the 
# workshop.
class Instructor:
    def __init__(self, name, expertise, years_of_experience):
        self.__name = name
        self.__expertise = expertise
        self.__years_of_experience = years_of_experience
        self.__workshops = []
        
class Participant:
    def __init__(self, name, registration_number, email):
        self.__name = name
        self.__registration_number = registration_number
        self.__email = email
        self.__enrolled_workshops = []
        self.__waitlisted_workshops = []
class Workshop:
    def __init__(self,name,instructor, date fee=1050, maximum_capacity=20):
        self.__workshop_name=name
        self.__workshop_instructor=instructor
        self.__workshop_fee= fee
        self.__workshop_maximum_capacity=maximum_capacity
        self.__workshop_date=date
        self.__enrolled_participants=[]
        self.__waitlist_participants=[]
        self.__attended_participants=[]

    def assign_instructor(self,instructor):
        self.__workshop_instructor = instructor 
    
    def enrolled_participants(self,participants):
        if len(__enrolled_participants)>= maximum_capacity:
           __waitlist_participants.append(participants)    
        else:
            _enrolled_participants.append(participants) 
               



