from collections import defaultdict
import random
from app.room import RoomClass, Office, Lspace
from app.employee import PersonClass, Fellow, Staff
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import random


# from database import Base


class Amity:
    def __init__(self):
        self.all_people = []
        self.all_rooms = []
        self.office_allocations = defaultdict(list)
        self.lspace_allocations = defaultdict(list)
        self.amity_unallocated = []
        self.fellows_list = []
        self.staff_list = []
        self.lspace_list = []
        self.office_list = []

    def create_room(self, room_name, room_type):

        if room_name in self.all_rooms:
            print("sorry, room already exists!please choose another name")

        else:
            if room_type.upper() == "LSPACE":
                room = Lspace(room_name, room_type)
                self.all_rooms.append(room)
                print("room successfully created")
            elif room_type.upper() == "OFFICE":
                room = Office(room_name, room_type)
                self.all_rooms.append(room)
                print("room successfully created")
            else:
                print("sorry, that room_type does not exist")

    def generate_room(self, r_type):
        available = []
        for room in self.all_rooms:
            if room.room_type == r_type.upper() and room.occupants <= room.max_occupants:
                available.append(room)

        if len(available) == 0:
            return None
        else:
            return random.choice(available)

    def create_person(self, person_name, person_description,
                      wants_accommodation):
        if person_name in self.all_people:
            print("sorry, this user already exists.please choose another name")
        else:
            if person_description.upper() == "STAFF":
                staff = Staff(person_name, person_description,
                              wants_accommodation)
                self.all_people.append(staff)
                self.staff_list.append(staff)
                print("person successfully created")

                allocated_office = self.generate_room("OFFICE")


                if allocated_office is not None:
                    self.office_allocations[allocated_office].append
                    (person_name.upper)
                    allocated_office.occupants += 1
                    print("congratulations %s, you have been assigned to office %s"
                              % (person_name, allocated_office.room_name))




                else:
                    self.amity_unallocated.append(person_name.upper)
                    print("sorry, all rooms are full at this time.")

            elif person_description.upper() == "FELLOW":
                fellow = Fellow(person_name, person_description,
                                wants_accommodation)
                self.all_people.append(fellow)
                self.fellows_list.append(fellow)
                allocated_office = self.generate_room("OFFICE")
                if allocated_office is not None:
                    self.office_allocations[allocated_office].append(person_name)
                    allocated_office.occupants += 1
                    print("congratulations %s, you have been assigned to office %s"
                          % (person_name, allocated_office.room_name))
                else:
                    self.amity_unallocated.append(person_name.upper() + "" + person_description)
                    print("sorry, all rooms are full at this time.")

                if wants_accommodation.upper() == "Y":
                    allocated_lspace = self.generate_room("LSPACE")
                    if allocated_lspace is not None:
                        self.lspace_allocations[allocated_lspace.room_name].append(person_name)
                        allocated_lspace.occupants += 1
                        print("congratulations %s, you have been assigned to lspace %s"
                              % (person_name, allocated_lspace.room_name))
                    else:
                        person = person_name.upper()
                        self.amity_unallocated.append(person)
                        print("sorry, all rooms are full at this time.")

                else:
                    print("user has been successfully created")

    def reallocate_person_to_lspace(self, person_name, new_room):
        room = Lspace(person_name, new_room)
        available_lspaces = [room.room_name for room in self.all_rooms if
                             room.room_type == "LSPACE" and room.occupants < room.max_occupants]
        if new_room in available_lspaces:
            if person_name in self.staff_list:
                print("sorry, staff cannot be assigned living spaces")
            elif person_name in self.fellows_list:
                if new_room.upper not in self.available_lspaces:
                    print("sorry, the room is not available")
                else:
                    reallocated_lspace = new_room
                    self.lspace_allocations.append(person.person_name.upper)

                    print("congratulations %s, you have been re-assigned to room %s"
                          % (person_name, reallocated_lspace))
        else:
            print("The room you chose is not available")

    def reallocate_person_to_office(self, person_name, new_room):
        room = Office()
        available_offices = [room.room_name for room in Amity.all_rooms if
                             room.room_type == "OFFICE" and room.occupants < room.max_occupants]
        if new_room in available_offices:
            self.office_allocations[new_room].append(person_name)
        else:
            print("The room you chose is not available")

    def load_people(self, filename):
        if filename:
            # file = file.txt
            with open(filename, 'r') as people_file:
                # filename_content = people_file.readlines()
                for line in people_file:
                    information = line.split()
                    first_name = information[0]
                    second_name = information[1]
                    full_name = first_name + " " + second_name
                    description = information[2]
                    if len(information) == 4:
                        wants_accommodation = information[3]
                    else:
                        wants_accommodation = "N"
                    self.create_person(person_name=full_name,
                                       person_description=description,
                                       wants_accommodation=wants_accommodation)
                    print("adding people...")

        else:
            print("please provide a text file")

    def print_allocations(self, filename=None):
        print("-" * 30 + "\n" + "AMITY ALLOCATIONS\n" + "-" * 30)

        #print(self.office_allocations)
        for office, name in self.office_allocations.items():
            print(office.room_name)
            print("-" * 30)
            print("\n")
            print(name)
            print("\n")

        if filename:
            file = open(filename + ".txt", "a")
            file.write("-" * 30 + "\n")
            for office in self.office_allocations:
                file.write("/n" + office.room_name + "/n")
                file.write("-" * 30 + "\n")
                for name in self.office_allocations[office]:
                    file.write(name + ", " )
                file.write("\n")

    def print_unallocated(self, filename=None):
        print("-" * 30 + "\n" + "amity_unallocated\n" + "-" * 30)
        if len(self.amity_unallocated)!=0:
            for person in self.amity_unallocated:
                print(person)
        else:
            print("All people have been allocated rooms!")
            if filename:
                file = open(filename + ".txt", "a")
                for person in self.amity_unallocated[person]:
                    file.write(person)



    def print_room(self, room_name):
        print("-" * 30 + "\n" + room_name + "\n" + "-" * 30)
        for room,person in self.lspace_allocations.items() :
            print(person)
