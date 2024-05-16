# Two-Factor Authentication (2FA) 🛡️

<hr>

## Table of Contents

- [Introduction](#introduction)
- [Running the App with Docker](#running-the-app-with-docker)
- [Application Flow](#application-flow)

## Introduction

This Python project aims to enhance skills and learn new concepts related to Two-Factor Authentication (2FA) implementations. 2FA adds an extra layer of security by requiring not only a password and username but also something that only the user has on them—such as a physical token.

## Running the App with Docker 🐳

To run the application using Docker, follow these steps:

1. Navigate to the `twoFactorAuth` directory in your terminal.
2. Execute the command `make docker-up`.
3. This command will create an instance of PostgreSQL and the application, which will be accessible at `0.0.0.0:8000/`.

## Application Flow

The application flow of Two-Factor Authentication (2FA) follows these steps:

1. **Create User**: 
   - API POST `/users/create` is used to create a new user. It returns a token to validate the email.

2. **Verify Email**: 
   - API POST `/auth/verify-mail/{token}` is used to validate the email. It returns a JSON containing:
     - `qrcode_otp`: Base64 encoded QR code to add the user to Google Authenticator.
     - `code_otp`: Secret to manually enter if a camera cannot be used.

3. **User Login**:
   - API POST `/auth/login` is used to log in with a username and password. It returns:
     - `otp_validation_token`: Token to validate the session in the next API call.

4. **Verify OTP**:
   - API POST `/auth/otp/verify` is used to validate the OTP and return an access token and a refresh token.
