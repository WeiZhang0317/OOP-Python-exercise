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
class Workshop:
    def __init__(self,name,instructor, fee, maximum_capacity, date):
        self.__workshop_name=name
        self.__workshop_instructor=instructor
        self.__workshop_fee= fee
        self.__workshop_maximum_capacity=maximum_capacity
        self.__workshop_date=date
        self.__enrolled_participants=[]
        self.__waitlist_participants=[]
        self.__attended_participants=[]



