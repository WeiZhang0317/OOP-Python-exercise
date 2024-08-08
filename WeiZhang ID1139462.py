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
            self.__workshop_name = name
        else:
            raise ValueError("Name must be a non-empty string")
    
    @property    
    def instructor(self):    
        """ Getter for the name attribute."""
        return self.__workshop_instructor  
    
    @instructor.setter
    def instructor(self, instructor):
        """ Setter for the instructor attribute. Must be an instance of Instructor."""
        if isinstance(instructor, Instructor):
            self.__workshop_instructor = instructor
        else:
            raise ValueError("Instructor must be an instance of the Instructor class")
    
    
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
        """ Validate the date format to be YYYY-MM-DD."""
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            return False
        
    @property
    def waitlist_participants(self):
        """ Getter for the waitlist participants attribute."""
        return self.__waitlist_participants

    def num_waitlist_participants(self):
        """ Return the number of participants on the waitlist."""
        return len(self.__waitlist_participants)

    def assign_instructor(self,instructor):
          """ Assign an instructor to conduct the workshop.  """ 
          self.instructor = instructor  
    
    

    def enroll_participant(self, participant):
        """ Enroll a participant to the workshop. If the workshop is full, the participant will be 
            added to the waitlist and the participant's waitlist will be updated.""" 
        if len(self.__enrolled_participants) < self.__workshop_maximum_capacity:
            self.__enrolled_participants.append(participant)
        else:
            self.__waitlist_participants.append(participant)
            participant.add_to_waitlist(self)




    def display_enroll_participant(self):
        """ Display all participants currently enrolled in the workshop."""
        result = "Enrolled participants: "
        for participant in self.__enrolled_participants:
            result += participant.name + ", "
        return result.rstrip(', ')


    
    def num_enrolled_participants(self): 
        '''Return the number of participants currently enrolled in the workshop'''
        return len(self.__enrolled_participants)
    
    def num_available_slots(self):
        '''  Return the number of available slots for enrolment in the workshop.  '''
        return self.__workshop_maximum_capacity-self.num_enrolled_participants()
    
    def remove_participant(self,participant): 
        '''  Remove a participant from the enrolled list of the workshop.'''  
        if participant in self.__enrolled_participants:
            self.__enrolled_participants.remove(participant)
        else:
            pass
    
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
                print(f"{participant.name} has already been marked as attended.")
        else:
            print(f"{participant.name} is not enrolled in this workshop.")
            
    def num_attended_participants(self):
        """Return the number of participants who attended the workshop"""
        return len(self.__attended_participants)        

    def cal_attendance_percentage(self):
        '''Calculate and return the attendance percentage for the workshop, representing 
           the ratio of participants attended to the total number of enrolled participants. '''
        total_attended_participants=len(self.__attended_participants)
        total_enrolled__participants=len(self.__enrolled_participants)
        if total_enrolled__participants == 0:
           return 0.0  
        attendance_percentage=(total_attended_participants/total_enrolled__participants)*100
        return attendance_percentage
    
    def __str__(self):
        '''Return a string representation of the workshop.'''
        return (
            f"Workshop Name: {self.__workshop_name}, "
            f"Instructor: {self.__workshop_instructor}, "
            f"Date: {self.__workshop_date}, "
            f"Enrolled Participants: {len(self.__enrolled_participants)}, "
            f"Available Slots: {self.num_available_slots()}, "
            f"Waitlist Participants: {len(self.__waitlist_participants)}"
        )
           
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
            self.__instructor_name = name
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
            "The name of the instructor is: " + self.__instructor_name +
            ", the expertise is: " + self.__expertise +
            ", and the years of experience is: " + str(self.__years_of_experience)
        )
    
    def add_workshop(self, workshop):
        ''' Add workshop to the instructor.''' 
        self.__workshops_assigned .append(workshop)

    def display_workshops(self):
        """ Display the list of tech workshops added to the instructor. """
        return (
            "The list of tech workshops added to " + self.__instructor_name +
            " is: " + ", ".join([workshop.name for workshop in self.__workshops_assigned])
        )
    
    def __str__(self):
        '''Return the instructor's profile.'''
        return self.instructor_profile()

    

class Participant:
    '''This class is to initialize the participant name, registration number, email address attributes'''
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
        if workshop.num_available_slots() > 0:
            workshop.enroll_participant(self)
            self.__participant_enrolled_workshops.append(workshop)
        else:
            workshop.enroll_participant(self)

                    
    def unenroll(self, workshop):
        """Unenroll from a tech workshop. """
        if workshop in self.__participant_enrolled_workshops:
            self.__participant_enrolled_workshops.remove(workshop)
            workshop.remove_participant(self)
        else:
            pass    
    
    def display_booked_workshops(self):
        '''Display all booked tech workshops.'''
        return ", ".join([workshop.name for workshop in self.__participant_enrolled_workshops])
    
    def add_to_waitlist(self, workshop):
        """Add the workshop to the participant's waiting list."""
        self.__participant_waiting_workshops.append(workshop)

    
    def __str__(self):
        '''Return participant's profile.'''
        return f"Name: {self.__participant_name}, Registration Number: {self.__registration_number}, Email: {self.__email}"

# Driver Program

def driver_program():
    # Create 2 Workshop objects
    workshop1 = Workshop("COMP646 WORKSHOP","Dr.Richard", "2024-09-01")
    workshop2 = Workshop("COMP330 WORKSHOP","Dr.Stuart", "2024-08-01")
    
    # Create 6 Participant objects
    # (self, name, registration_number, email):
    participants = [
    Participant("Wei","021069","Wei@Lincoln.ac.nz"),
    Participant("Lilian","023362","Lilian@Lincoln.ac.nz"),
    Participant("William","189521","William@Lincoln.ac.nz"),
    Participant("Wade","655844","Wade@Lincoln.ac.nz"),
    Participant("Kiko","544952","Kiko@Lincoln.ac.nz"),
    Participant("Ian","45451","Ian@Lincoln.ac.nz"),  
     ]
    
    
    # Create 2 Instructor objects
    instructor1 = Instructor("Dr.Richard", "Artificial Intelligence", 20)
    instructor2 = Instructor("Dr.Stuart", "Data Science", 12)

     # Assign an instructor to each workshop
    workshop1.assign_instructor(instructor1)
    workshop2.assign_instructor(instructor2)
    
     # Add workshops to instructors
    instructor1.add_workshop(workshop1)
    instructor2.add_workshop(workshop2)

    # Set up at least 5 participant bookings for each workshop
    # Book all participants into workshop1 COMP646
    for participant in participants:
        participant.book_workshop(workshop1)
     
    
     # Book some participants into workshop2 COMP644
    for participant in participants[:5]:  #only the first 5 participants book for workshop2
        participant.book_workshop(workshop2) 
    
    # Cancel a participant's enrolment in a specific tech workshop. 
    participants[2].unenroll(workshop1)
    
    # Record 2 specific participants checking into a tech workshop. 
    workshop1.mark_attendance(participants[0])
    workshop1.mark_attendance(participants[1])
    
    # Display the number of available slots for a tech workshop.
    print(f"The available slots for {workshop1.name} is {workshop1.num_available_slots()}")

   # Display the waiting list for a workshop
    if workshop1.waitlist_participants:
        print("Waiting list for {} is:".format(workshop1.name))
        for participant in workshop1.waitlist_participants:
            print(participant.name)
    else:
        print("No participants on the waiting list for {}.".format(workshop1.name))
        
    # Display the number of waitlist participants in a tech workshop.
    print(f"Number of waitlist participants in {workshop1.name} is {workshop1.num_waitlist_participants()}")

        
        
    # Display the list of enrolled participants for a tech workshop. 
    print(workshop1.display_enroll_participant())
    # Display the number of participants enrolled in a tech workshop.
    print(f"Number of participants enrolled in {workshop1.name} is {workshop1.num_enrolled_participants()}") 
    # Display the number of waitlist participants in a tech workshop. 
    print(f"Number of waitlist participants in {workshop1.name} is {len(workshop1._Workshop__waitlist_participants)}")
    # Display the number of attendees for a tech workshop. 
    print(f"Number of attendees for {workshop1.name} is {workshop1.num_attended_participants()}")
    # Display the attendance percentage for a tech workshop. 
    print(f"Attendance percentage for {workshop1.name} is {workshop1.cal_attendance_percentage()}%")
    # Display the total payment collected for a tech workshop
    print(f"Total payment collected for {workshop1.name} is ${workshop1.calculate_payment()}")
    
    # Display the list of workshops hosted by a particular instructor along with the full profile details of the instructor
    print(instructor1.display_workshops())
    print(instructor1)
    
    # Display the list of tech workshops for which a specific participant is enrolled
    print(f"{participants[0].name} is enrolled in the following workshops: {participants[0].display_booked_workshops()}")

driver_program()
