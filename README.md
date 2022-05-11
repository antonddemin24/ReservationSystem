# Reservation system

## Introduction

The program saves information about reservations into a calendar and marks the chosen resources as reserved for that time. When making a reservation causes a conflict (the resource has already been reserved), the reservation doesn’t go through. The program adds relevant information on the customer to each reservation. The program can be used to check the reservations on a given point of time and to print out information on reservations within a time interval determined by the user.

## File and directory structure

The project consists of code files and documentation, which is located in the documentation folder.

## Installation instructions

PyQt5 and standard python libraries like datetime, calendar used in the program.

## User instructions

Program should be run using main1.py file and running main part of the program.

Firstly, user should enter customer number (like "123456"). In tab 'Reservation' user can see all reservations for selected room.
User can change room selecting it and pressing 'Update'. When he decides on the dates he wants to choose, need enter it in format like '05,05,2021' and press 'Run'.
In tab 'Cancel reservation' user sees all his reservation and he could cancel it by entering Id of reservation.