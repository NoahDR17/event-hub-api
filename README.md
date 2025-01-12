# Event Hub

## Introduction
A web application built with React (front-end) and Django REST Framework (back-end) to create, discover, and discuss events.

## Technologies

---

## Agile 
### Epics 

 - Epic 1 API - Set up ( Done ) 
  - User Stories:
   - 1.1 Project set up ( Done )
   - 1.2 Cloudinary ( Done )

 - Epic 2 API - Profiles app ( Done )
  - User Stories:
   - 2.1 Create "profiles" app ( Done )
   - 2.2 Create Profile Model ( Done )
   - 2.3 Create Profile Serializer ( Done )
   - 2.4 Create Profile View ( Done )

 - Epic 3 API - Events app 
  - User Stories:
   - 3.1: Create "events" App - Must have ( Done )
   - 3.2: Tag Model - Must have ( Done )
   - 3.3: Event Model - Must have ( Done )
   - 3.4: Integrate Many-to-Many Tags - Should have ( Done )
   - 3.5: Location & Event Type - Could have ( Done )
   - 3.6: Basic CRUD and Permissions Integration - Should have ( Done )
   - 3.7: Event View and Serializer - Must have ( Done )

 - Epic 4 API - Create Comments, Likes, and Followers/Following Features
  - User Stories: 
   - 4.1: Create Comment Feature - Must Have ( In Progress )
...

## Features (Current State)

---

## Testing
### Tests During Development 
- Test Case 1 (Carried out during the initial stages of backend development/profile-setup): 
 - Verify Default Cloudinay Image.
  - Ensure that when no custom image is uploaded on profile creation, the application correctly assigns and displays a default image hosted on Cloudinary.

 - Steps:
  - Create Superuser, if one is already created then that one will work fine.
  - In the devepment server, navigate to "profile/" or "profile/{id}".
  - Check the image url of a profile.
  - Ensure url is "https://res.cloudinary.com/<cloud-name>/image/upload/v1/media/../name-of-image"

- Expected Outcome: 
 - The url is "https://res.cloudinary.com/<cloud-name>/image/upload/v1/media/../name-of-image"

- Actual Outcome: 
 - The url is "/name-of-image" 

- Fix:
 - From what i gathered while troubleshooting the old method of declaring the default media file storage has been depracated.
  - it is no longer " DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage' ", and instead is
    " STORAGES = {
            "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
            "default": {"BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage"},
        } " 
 - After making this change, image urls are what they were expected to be.
 - more tests can be carried out once more functionality has been implemented.
 ### Manual Tests

 ## Manual Test: Creating a New Tag During Event Creation ( ToDo )

### Purpose
Confirm that a user can seamlessly create a brand-new tag while creating an event in the front-end interface.

### Prerequisites
1. A valid, logged-in user account.  
2. An existing list of known tags (to verify we’re creating a *new* tag, not reusing an existing one).  
3. Functional front-end form or page that allows entering event details, including tags.

### Steps
1. **Log in**  
   - Open the web application in a browser.  
   - Log in with a valid user account (e.g., username: `testuser`, password: `password123`).  
   - Confirm you are successfully redirected to the home/dashboard page.

2. **Navigate to “Create Event” Page**  
   - Click on the “Create Event” or “New Event” button/link.  
   - Observe that the event creation form loads properly (title, description, location, date/time, tags, etc.).

3. **Fill Out Basic Event Details**  
   - Enter an **Event Title** (e.g., “Future Tech Workshop”).  
   - Enter a brief **Description** (e.g., “Hands-on exploration of new technologies.”).  
   - Select a **Date/Time** in the future.  
   - Enter a **Location** (city, venue name, etc.).  
   - (Optional) Upload an **Image**.

4. **Create a Brand-New Tag**  
   - In the tags section, type in a **new tag name** that does *not* currently exist in the system (e.g., Dog Friendly or Vegan).  
   - If the UI allows for multiple tags, add the new tag plus any existing tags as needed.  
   - Confirm you are either shown a “New Tag Created” indicator or that the front-end acknowledges you have entered a new tag.

5. **Submit the Event**  
   - Click the **Submit** or **Create Event** button.  
   - Wait for the success message or confirmation.

6. **Verify the Event Creation**  
   - After successful submission, you should see the newly created event in your events list or be redirected to the event detail page.  
   - Confirm the newly added tag is displayed alongside the event details (e.g., “Tags: Dog Friendly).

7. **Check Database or API (Optional Advanced Check)**  
   - Verify that the **Tag** model contains the new tag:'Dog Friendly' in the database.  
   - Check the **Event** entry to confirm its `tags` field includes the newly created tag ID.

### Expected Outcome
- The event is created with all entered fields (title, description, date/time, location, image).  
- The **newly created tag** is visible on the event detail view.  
- No errors or warnings appear during submission.  
- Users can search or filter by the new tag (if the front-end supports that feature).

--------------------------------------------

# Manual Test: Ensure Users Cannot Edit Another User's Profile

## Test Objective
Verify that a logged-in or logged-out user cannot edit another user's profile information.
---

## Test Steps

1. **Log in as `User A`:**
   - Navigate to the login form.
   - Enter `User A`'s credentials (username and password).
   - Click the **Login** button.

2. **Attempt to Edit `User B`'s Profile:**
   - Locate `User B`'s profile detail page eg = "/profiles/UserB_Id".

3. **Perform Editing Action:**
   - If an edit form appears, make changes to `User B`'s profile.
   - Click **Save** or **Submit** to attempt saving the changes.

---

## Expected Result
- `User A` is **not** able to access the edit form for `User B`'s profile.
- If `User A` attempts to submit changes directly (e.g., via URL manipulation):
- `User B`'s profile remains unchanged.

## Actual Result: When signed in as user A, i opened user B's ProfileDetail Page, and an edit form appeared, after editing the content of the profile, i submitted and the change was made.

## Fix: added permission classes to "profiles/views.py" file, and added logic to validate the object permissions before a get request can be sent.



### Automated Tests

---

## Deployment
- Deployed on Heroku at:

