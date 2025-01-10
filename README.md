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

 - Epic 2 API - Profiles app 
  - User Stories:
   - 2.1 Create "profiles" app ( Done )
   - 2.2 Create Profile Model ( Done )
   - 2.3 Create Profile Serializer ( Done )
   - 2.4 Create Profile View ( In Progress "Half Complete" )
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




### Automated Tests

---

## Deployment
- Deployed on Heroku at:

