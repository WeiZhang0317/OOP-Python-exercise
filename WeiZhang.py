from datetime import datetime 

class Workshop:
    def __init__(self,name,instructor,date):
        self.__workshop_name=name
        self.__workshop_instructor=instructor
        self.__workshop_fee= 1050
        self.__workshop_maximum_capacity=20
        self.__workshop_date=date
        self.__enrolled_participants=[]
        self.__waitlist_participants=[]
        self.__attended_participants=[]
    
    def get_name(self):    
        """ Getter for the name attribute."""
        return self.__workshop_name
    
    def set_name(self, name):
        """ Setter for the name attribute.Must be a non-empty string."""
        if isinstance(name, str) and name.strip():
            self.__workshop_name = name
        else:
           raise ValueError("Name must be a non-empty string")
        
    def get_instructor(self):    
        """ Getter for the name attribute."""
        return self.__workshop_instructor  
    
    def set_instructor(self, instructor):
        """ Setter for the instructor attribute. Must be a non-empty string."""
        if isinstance(instructor, str) and instructor.strip():
            self.__workshop_instructor = instructor
        else:
           raise ValueError("Instructor must be a non-empty string")    
    
    def get_fee(self):
        """ Getter for the fee attribute."""
        return self.__workshop_fee

    def get_maximum_capacity(self):
       """ Getter for the maximum_capacity attribute."""
       return self.__workshop_maximum_capacity
    
    def get_date(self):
        """ Getter for the date attribute."""
        return self.__workshop_date

    def set_date(self, date):
        """ Setter for the date attribute. Must be a valid date in YYYY-MM-DD format."""
        if self.validate_date(date):
            self.__workshop_date = date
        else:
            raise ValueError("Date must be in YYYY-MM-DD format and a valid date")
        
    @staticmethod
    def validate_date(date):
        """ Validate the date format to be YYYY-MM-DD and check if it's a valid date."""
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def assign_instructor(self,instructor):
          """ Assign an instructor to conduct the workshop.  """ 
          self.set_instructor(instructor)  

    def enroll_participant(self,participant):      
        """ Enroll an participant to the workshop. If the workshop is full, the participant will be 
            added to the waitlist.""" 
        if len(self.__enrolled_participants) < self.__workshop_maximum_capacity:
           self.__enrolled_participants.append(participant)
           print(f"{participant.get_name()} is enrolled in {self.__workshop_name}.")
        else:   
            self.__waitlist_participants.append(participant)

    def display_enroll_participant(self):
      ''' Display all participants currently enrolled in the workshop.'''
      result = "Enrolled participants: "
      for participant in self.__enrolled_participants:
       result += participant.get_name() + ", "
       return result.rstrip(', ')
    
    def num_enrolled_participants(self): 
        '''Return the number of participants currently enrolled in the workshop'''
        return len(self.__enrolled_participants)
    
    def num_available_slot(self):
        '''  Return the number of available slots for enrolment in the workshop.  '''
        return self.__workshop_maximum_capacity-self.num_enrolled_participants()
    
    def remove_participants(self,participant): 
        '''  Remove a participant from the enrolled list of the workshop.'''  
        return self.__enrolled_participants.remove(participant)
    
    def calculate_payment(self):
        '''Calculate and return the total payment received for the workshop based on the 
           number of enrolled participants and the workshop fee. '''     
        if self.num_enrolled_participants()==0:
             return self.__workshop_fee
        else:
            return  self.num_enrolled_participants()* self.__workshop_fee
    
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
    
    def check_capacity(self,workshop):
        '''Check if workshop is already full, if so the participant will be added to waitlist.'''
         if len



 

