# Touch - Local Community
## Introduction
___

**Touch** is a vibrant and supportive community platform designed to foster mutual assistance among its members. Our community encompasses a diverse range of topics, including:

* **Gardening**: Share your gardening tips, seek advice on plant care, and connect with fellow gardening enthusiasts. Whether you're a seasoned gardener or just starting out, this is the place to cultivate your green thumb.

* **House Work**: From cleaning hacks to home maintenance, discuss all aspects of housework. Exchange ideas on making household chores more efficient and discover new ways to keep your home in top shape.

* **After School**: A dedicated space for parents, students, and educators to discuss after-school activities. Share resources, plan extracurricular activities, and support each other in balancing schoolwork and leisure.

* **Question**: Have a question that needs an answer? Post it here and let the community help you out. From practical advice to detailed explanations, get the support you need from knowledgeable members.

* **Others**: This category covers a wide array of miscellaneous topics that don't fit into the other categories. It's a catch-all for discussions on hobbies, personal projects, and more.

Touch is more than just a forum—it's a community where members help each other thrive. Join us today and be a part of a supportive network that values sharing, learning, and growing together.


## Team Member
___

|  Name   | Student ID |
|  ----  |------------|
| Xiang Li  | 23921151   |
| Wannian Mei  | 单元格        |
| Hangqiuzi Wang | 单元格        |
| Chang Chen  | 单元格        |

## Virtual Environment Setup
___

A Virtual Environment is necessary to develop and test the application. This is
performed in a safe, self-contained manner through Python's Virtual
Environment.

### 1. Initialise a Python Virtual Environment
Ensure that your current working directory contains the `requirements.txt`
file, in this case it is '/venv', then use:

`$ python -m venv venv`

NOTE: Your system may have `python3` aliased as something other than `python`

### 2. Activate the new Virtual Environment

On standard Unix operating systems this would be:

`$ source venv/bin/activate`

On Windows systems:

`$ venv\Scripts\activate`

### 3. Install Requirements

The `requirements.txt` file contains all the Python dependencies that the
application requires to run. These can be downloaded and installed with:

`$ pip install -r requirements.txt`

NOTE: Your system may have `pip3` aliased as something other than `pip`

### 4. Start the server

To start the server and open pages in our browser, the follow command should be executed:

`python app.py`

## Module Design
___
### 1. Auth Module

#### Function Overview

The Auth Module handles user registration, login, logout,It also includes security questions for password recovery.

#### Main Features

- **Registration**: Users can register by providing a username, email, password, security question, and answer.
- **Login**: Registered users can log in using their email and password.
- **Logout**: Logged-in users can log out.
- **Security Questions**: Users can set and answer security questions for password recovery.

#### Main Files

- `app/models.py`: Defines the `UserModel` and related methods.
- `app/forms.py`: Defines the `RegisterForm` and `LoginForm`.
- `app/blueprint/auth/auth.py`: Handles user registration, login, and logout views and routes.
- `app/templates/`: Contains HTML templates (login.html,register.html,forgot-password.html,register.html).

### 2. Post and Comment Module

#### Function Overview

The PostCom Module allows users to create post, view and search. Users can comment on posts and mark the best answer.

#### Main Features

- **Create Post**: Users can create new posts by providing a title, content, type, and postal code.
- **View Post**: Users can view post details and comments.
- **Comments**: Users can comment on posts.
- **Best Answer**: Post authors can mark a comment as the best answer.

#### Main Files
- `app/models.py`: Defines the `PostModel` and `CommentModel` and related methods.
- `app/forms.py`: Defines the `PostForm` and `CommentForm`.
- `app/blueprint/postCom/postCom.py`: Handles post-related views and routes.
- `app/templates/`: Contains HTML templates for posts and comments(post-detail.htm,posts.htmll).

### 3. Profile Module

#### Function Overview

The Profile Module allows users to manage their profile settings, including changing their avatar and username, viewing their own posts and comments, and deleting their posts and comments.

#### Main Features

- **Change Avatar**: Users can upload a new avatar image.
- **Change Username**: Users can update their username.
- **View Posts and Comments**: Users can view their own posts and comments.
- **Delete Posts and Comments**: Users can delete their own posts and comments.

#### Main Files

- `app/models.py`: Defines the `UserModel`, `PostModel`, and `CommentModel`.
- `app/forms.py`: Defines the forms used in the profile management process (`EditUsernameForm`, `UploadImageForm`).
- `app/blueprint/profile/profile.py`: Handles profile-related views and routes.
- `app/templates/`: Contains HTML templates (`profile.html`).


### 4. Notification Module

#### Function Overview

The Notification Module is responsible for sending notifications to users when their posts or comments receive replies.

#### Main Features

- **Generate Notifications**: Generate a notification when a user's post or comment receives a reply.
- **View Notifications**: Users can view unread notifications.
- **Delete Notifications**: Users can delete read notifications.

#### Main Files

- `app/models.py`: Defines the `Notifications` model and related methods.
- `app/blueprint/notification/notification.py`: Handles notification-related views and routes.
- `app/templates/`:ajax rendering on `base.html`

## Responsive Design
___
#### 768*800
![responsive_768*800.jpg](docs%2Fresponsive_768*800.jpg)
#### 1025*800
![responsive_1024*800.jpg](docs%2Fresponsive_1024*800.jpg)
![responsive_768*800_1.jpg](docs%2Fresponsive_768*800_1.jpg)