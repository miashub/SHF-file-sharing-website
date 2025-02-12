# Reflection
Study your assignment part1 solution, reread the related part of the course notes, and ensure you have understood the concepts covered by this assignment. Write your answer here to the assignment questions (Check the assignment instructions)

1) We carefully read through the assignment instructions multiple times to ensure we understood each requirement, like implementing secure file uploads, encryption, user authentication, and file sharing. 
Breaking down the requirements into smaller actionable steps helped us to speed the development process. For example, we tackled user registration and login first before moving to file-related functionalities.

We were initially not sure about how file sharing should function, particularly whether shared files should be visible to all users or only to specific individuals. To resolve this, we reread the assignment notes and consulted the course materials. The use of ManyToMany relationships in Django models ultimately provided a clear solution for selective sharing.
Another area that required clarification was how to implement encryption. We werent sure whether to encrypt files only during transmission or also at rest in the database. After reviewing related lectures, we decided to encrypt files before saving them in the database to ensure security even in the event of a database breach.
To help with some clarifications we revisited relevant course modules on Django, database relationships, and security best practices to find answers. This helped clarify implementation strategies, such as using Django ORM for managing relationships and ensuring data integrity.
 For unclear technical aspects, we set up small prototype projects to test solutions before implementing them in the main application. For example, we tested how file encryption with Fernet would integrate with file uploads in Django.


2)We chose Django for its huge developed feature set, which included built-in user authentication, ORM for database management, and security features like CSRF protection and XSS prevention.
We also considered alternative frameworks like Flask but it lacked the built-in functionality Django provides. While Flask offers flexibility, using Django reduced development time and aligned well with the requirements of this assignment.
Django's emphasis on rapid development and scalability made it a practical choice for this project.

For Authentication we used Django’s User model for user management and its authenticate method to handle login securely.
Also we used  CSRF tokens in forms to ensure security during registration and login.
In the case of file upload and encryption, the files were stored as binary data in the database after being encrypted with cryptography.fernet.
File integrity was ensured using SHA-256 hashing, stored alongside the encrypted content.
For scalability we used a modular design with separate views for file upload, download, and sharing to keep functionalities independent and easy to maintain.We also designed the EncryptedFile model with a ManyToManyField for flexible sharing options, enabling future features like group sharing without significant changes.

3) Encryption is very important to protect sensitive user files from unauthorized access, both in transit and at rest.
It makes sure of data confidentiality and prevents malicious actors from reading or tampering with files even if they have access to the database or server.
By encrypting the files, the application provides an added layer of trust, giving confidence to the users that their private data is secure and safe.

We used encryption using Fernet, a symmetric encryption scheme provided by the cryptography library.
The encryption key was loaded from a secure environment variable, ensuring it wasn't hardcoded into the application, which would pose a security risk.
Each file uploaded by the user was encrypted before being stored in the database, and a SHA-256 hash was generated for integrity verification.

Some challenges we encountered included:
Managing the encryption key securely, as losing the key would render all encrypted files unreadable.
Handling large files efficiently, as the encryption process can increase memory and CPU usage, which needed optimization.
Debugging errors in the decryption process, which were often caused by encoding issues or corrupted files.

Access to files is controlled by associating each file with the uploading user through a foreign key relationship in the EncryptedFile model.
Only the owner of a file or users it has been explicitly shared with can access or download the file.
Unauthorized access was prevented by:
Django’s built-in authentication and @login_required decorators to restrict access to authenticated users only.
Explicit checks in views to ensure that the current user is authorized to view or download the requested file.
Secure sharing features where users can only share files with valid, registered users in the application.
Environment variables for storing sensitive keys, reducing the risk of exposure.
Comprehensive error handling to avoid leaking file information through error messages.


4) 
To make sure of modularity and organization in our code:
We followed Django’s Model-View-Template (MVT) architecture, which naturally promotes modularity by separating the data (models), logic (views), and presentation (templates).
Each feature like user authentication, file encryption, or sharing, was implemented as a self-contained component. For example:
User authentication  was handled through separate views (login_view, register, logout_view) and associated forms (LoginForm, RegistrationForm), which kept logic independent and reusable.
File encryption and management was implemented in the EncryptedFile model, with clearly defined methods and properties to handle encryption, file storage, and integrity verification.
File sharing was encapsulated in specific views like share_file and designed to work with Django's ORM relationships.
IWe avoided redundant code by using helper functions and built-in utilities. For example, using get_object_or_404 in views instead of manually querying and handling errors.
The use of environment variables and configuration files separated sensitive information and reusable settings, making the application easier to configure across environments.

The benefits of this approach for future development or when adding new features are:
Its easy tio maintain.Changes to one part of the code like views don’t affect others like models or templates, reducing the risk of introducing bugs.
The modular structure makes it straightforward to add new features, like file previews or advanced sharing options, without rewriting existing functionality.
Components like the forms and error-handling mechanisms can be reused in other projects, saving development time.
 Clear separation of concerns makes it easier for new developers to understand the codebase.

The parts of the code do you consider most reusable are:
 Both RegistrationForm and LoginForm are reusable in any project that requires user authentication. They encapsulate field validation and presentation in a modular way.
The EncryptedFile model is reusable in other projects that involve secure file management. Its methods for file hashing and encryption are generic and well-encapsulated.
Patterns like using get_object_or_404 and displaying meaningful messages with messages are reusable for improving the efficiency of other applications.
 The encryption and hashing logic can be adapted to any application requiring secure data storage, given it is implemented independently of other logic.

5) To improve user experience we made use of various error handling methods. When users submit invalid data, we made sure that clear, understandable feedback was provided. For example, in the login and registration forms, if the credentials were incorrect or a required field was missing, users received specific messages indicating what went wrong.
If a user enters an incorrect password, the form displays a message "Invalid username or password," helping users identify and correct the issue without frustration.

This prevents attackers from finding out valid usernames and focuses only on the validity of the password which was entered.
Example, The login form provides feedback like "Invalid username or password," but without specifying whether the issue lies with the username or password which makes a safer user experience.

For views such as file uploads, downloads, and sharing, we used Django’s @login_required decorator to ensure that only authenticated users could access these functionalities. If an unauthorized user attempts to access these views, they are redirected to the login page.
This approach prevents unauthorized users from trying to access sensitive resources.

To prevent issues with unsupported file types, we checked the file format before going with the file upload. If the uploaded file was not of a supported type like non-image or non-text file types, we added validation logic to reject the file upload and provided an error message like "Unsupported file type. Please upload a valid file."
This ensured the application only handled files that could be properly encrypted and managed within the app.

Also with user-facing error messages, we used Django’s logging system to log unexpected errors, such as server-side issues or database connection failures. This allows us to track and diagnose problems properly, even if they don’t directly affect the user experience.



6) Some secure coding practices we applied and how they protect against common vulnerabilities such as SQL injection and XSS are:

We used Django’s ORM for database interactions, which automatically handles parameterized queries. This eliminates the risk of SQL injection, as it ensures user inputs are safely escaped before being included in database queries.
For example, filtering records like EncryptedFile.objects.filter(user=request.user) prevents directly embedding user input into raw SQL queries, reducing potential vulnerabilities.

Django’s built-in CSRF protection was enabled by default, and we ensured it was applied to all forms handling sensitive user data. This stops attackers from forging requests on behalf of authenticated users.
In templates like register.html, the {% csrf_token %} tag was included to ensure all form submissions were secure.

User inputs displayed on the frontend were properly escaped using Django’s templating engine, which escapes potentially harmful characters by default. This protected against XSS  by preventing malicious scripts from being injected into rendered pages.
For example, if a malicious user entered <script>alert('XSS')</script> in a form, Django’s escaping would render it as plain text, making this attack useless.

The encryption key and other sensitive information were stored securely in environment variables rather than hardcoding them in the application code. This mitigates risks associated with code exposure, like accidentally sharing of secrets in public repositories.

We implemented strict access control mechanisms using Django’s authentication system. For example, only logged-in users could upload, download, or share files.
Encrypted files were filtered to show only those belonging to the logged-in user or shared explicitly with them.
We believe the application is reasonably secure for its scope and follows practices such as input validation, access control, encryption, and protection against SQL injection and XSS.
The use of encryption ensures files are secure at rest, and CSRF protection adds a layer of safety for user interactions.

Some potential improvements we would use are:
Adding detailed logging for all file-related activities uploads, downloads, sharing would improve traceability and help detect unauthorized actions or suspicious behavior.

Strengthening password validation during registration by creating rules like a mix of uppercase, lowercase, numbers, and special characters.



7) Advantages of Github Codespace include:

GitHub Codespace provided a cloud-based development environment that was consistent across different machines. We didn't have to worry about setting up local development environments, managing dependencies, or configuring our setup on multiple devices. It was especially useful for ensuring that everyone working on the project had the same environment.

Because it was cloud-based, GitHub Codespace offered integration with GitHub. This allowed for easy access to the project repository, making version control and collaboration more efficient. We could easily pull changes, commit updates, and track issues directly from the IDE speeding up the development process.

GitHub Codespace integrates with a variety of tools such as the terminal, debugger, and browser for live testing. This made testing code, debugging, and deploying features straightforward. For example, we could run the Django development server directly from the environment and quickly test our changes.

Some limitations are:
Since GitHub Codespace relies on cloud connectivity, any internet disruptions could slow down development. Slow internet speeds impact the workflow, especially when interacting with the GitHub repository. The window logs out too quickly due to lack of activity for even 2 minutes.

While GitHub Codespaces offer good performance, for larger projects or more resource-intensive operations liike working with large datasets or running complex algorithms, it may feel slower than working on a local machine with more dedicated resources.