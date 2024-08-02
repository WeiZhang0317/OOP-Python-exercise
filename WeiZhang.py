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
    
    @property
    def name(self):
        """ Getter for the name attribute."""
        return self.__workshop_name    
    
    @name.setter
    def name(self, name):
        """ Setter for the name attribute. Must be a non-empty string."""
        if isinstance(name, str) and name.strip():
            self.__name = name
        else:
            raise ValueError("Name must be a non-empty string")
    
    @property    
    def instructor(self):    
        """ Getter for the name attribute."""
        return self.__workshop_instructor  
    
    @instructor.setter
    def instructor(self, instructor):
        """ Setter for the instructor attribute. Must be a non-empty string."""
        if isinstance(instructor, str) and instructor.strip():
            self.__workshop_instructor = instructor
        else:
           raise ValueError("Instructor must be a non-empty string")    
    
    @property    
    def fee(self):
        """ Getter for the fee attribute."""
        return self.__workshop_fee
    
    @property
    def maximum_capacity(self):
       """ Getter for the maximum_capacity attribute."""
       return self.__workshop_maximum_capacity
    
    @property
    def date(self):
        """ Getter for the date attribute."""
        return self.__workshop_date
    
    @date.setter
    def date(self, date):
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
          self.instructor(instructor)  

    def enroll_participant(self,participant):      
        """ Enroll an participant to the workshop. If the workshop is full, the participant will be 
            added to the waitlist.""" 
        if len(self.__enrolled_participants) < self.__workshop_maximum_capacity:
           self.__enrolled_participants.append(participant)
           print(f"{participant.get_name()} is enrolled in {self.__workshop_name}.")
        else:   
            self.__waitlist_participants.append(participant)

    def display_enroll_participant(self):
        """ Display all participants currently enrolled in the workshop."""
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
        return  self.num_enrolled_participants()* self.__workshop_fee
    
    def mark_attendance(self,participant):
        '''Mark a participant's attendance for the workshop.'''
        if participant in self.__enrolled_participants:
            if participant not in self.__attended_participants:     
                self.__attended_participants.append(participant)
            else:
                print(f"{participant.get_name()} has already been marked as attended.")
        else:
            print(f"{participant.get_name()} is not enrolled in this workshop.")

    def cal_attendance_percentage(self):
        '''Calculate and return the attendance percentage for the workshop, representing 
           the ratio of participants attended to the total number of enrolled participants. '''
        total_attended_participants=len(self.__attended_participants)
        total_enrolled__participants=len(self.__enrolled_participants)
        if total_enrolled__participants == 0:
           return 0.0  
        attendance_percentage=(total_attended_participants/total_enrolled__participants)*100
        return attendance_percentage
           
class Instructor:
    '''This class is to initialize the
    instructor name, expertise, and experience attributes.'''
    
    def __init__(self, name, expertise, years_of_experience):
        self.__instructor_name = name
        self.__expertise = expertise
        self.__years_of_experience = years_of_experience
        self.__workshops_assigned = []

    @property
    def name(self):
        """ Getter for the name attribute."""
        return self.__instructor_name    
    
    @name.setter
    def name(self, name):
        """ Setter for the name attribute. Must be a non-empty string."""
        if isinstance(name, str) and name.strip():
            self.__name = name
        else:
            raise ValueError("Name must be a non-empty string")

    @property
    def expertise(self):
        """ Getter for the expertise attribute."""
        return self.__expertise

    @expertise.setter
    def expertise(self, expertise):
        """ Setter for the expertise attribute. Must be a non-empty string."""
        if isinstance(expertise, str) and expertise.strip():
            self.__expertise = expertise
        else:
            raise ValueError("Expertise must be a non-empty string")
    
    @property
    def years_of_experience(self):
        """ Getter for the years_of_experience attribute."""
        return self.__years_of_experience 
    
    @years_of_experience.setter
    def years_of_experience(self, years_of_experience):
        """ Setter for the years_of_experience attribute. Must be a non-negative integer."""
        if isinstance(years_of_experience, int) and years_of_experience >= 0:
            self.__years_of_experience = years_of_experience
        else:
            raise ValueError("Years of experience must be a non-negative integer")

    def instructor_profile(self):
        ''' Display the instructor's full profile, including name, expertise, and experience. '''
        return (
            "The name of the instructor is: " + self.__name +
            ", the expertise is: " + self.__expertise +
            ", and the years of experience is: " + str(self.__years_of_experience)
        )
    
    def add_workshop(self, workshop):
        ''' Add workshop to the instructor.''' 
        self.__workshops_assigned .append(workshop)

    def display_workshop(self):
        """ Display the list of tech workshops added to the instructor. """
        return (
            "The list of tech workshops added to " + self.__name +
            " is: " + ", ".join([workshop.name for workshop in self. self.__workshops_assigned])
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
        self.__participant_name = name
        self.__registration_number = registration_number
        self.__email = email
        self.__participant_enrolled_workshops = []
        self.__participant_waiting_workshops = []
    
    @property
    def name(self):
        """ Getter for the name attribute."""
        return self.__participant_name
    
    @name.setter
    def name(self, name):
        """ Setter for the name attribute. Must be a non-empty string."""
        if isinstance(name, str) and name.strip():
            self.__participant_name = name
        else:
            raise ValueError("Name must be a non-empty string")
    
    @property
    def registration_number(self):
        """ Getter for the registration number attribute."""
        return self.__registration_number
    
    @registration_number.setter
    def registration_number(self, registration_number):
        """ Setter for the registration number attribute. Must be a non-empty string."""
        if isinstance(registration_number, str) and registration_number.strip():
            self.__registration_number = registration_number
        else:
            raise ValueError("Registration number must be a non-empty string")
    
    @property
    def email(self):
        """ Getter for the email attribute."""
        return self.__email
    
    @email.setter
    def email(self, email):
        """ Setter for the email attribute. Must be a valid email address."""
        if isinstance(email, str) and email.strip() and "@" in email:
            self.__email = email
        else:
            raise ValueError("Email must be a valid email address")
        
    def book_workshop(self, workshop):
        """Book enrolment in a tech workshop. If the workshop is already full, the participant will be added to the waitlist. """
        if workshop.num_available_slot()>0:
            workshop.enroll_participant(self)
            self.__participant_enrolled_workshops.append(workshop)  
            print(f"{self.__participant_name} is enrolled in {workshop.name}.")
        else:
            workshop.__waitlist_participants.append(self)
            self.__participant_waiting_workshops.append(workshop) 
            print(f"{self.__participant_name} is added to the waitlist for {workshop.name}.")
                
    def unenroll_workshop(self, workshop):
        """Unenroll from a tech workshop."""
        if self.__participant_name in workshop.__enrolled_participants:
    
    
    
    
    
    
    
    # def unenroll(self, workshop):
    #     '''Unenroll from a tech workshop.'''
    #     if workshop in self.__enrolled_workshops:
    #         self.__enrolled_workshops.remove(workshop)
    #         workshop.remove_participants(self)
    #         print(f"{self.__participant_name} has been unenrolled from {workshop.name}.")
    #     else:
    #         print(f"{self.__participant_name} is not enrolled in {workshop.name}.")
    
    def display_booked_workshops(self):
        '''Display all booked tech workshops.'''
        return ", ".join([workshop.name for workshop in self.__enrolled_workshops])
    
    def __str__(self):
        '''Return participant's profile.'''
        return f"Name: {self.__participant_name}, Registration Number: {self.__registration_number}, Email: {self.__email}"



 

