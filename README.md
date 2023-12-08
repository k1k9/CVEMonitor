# CVE Monitor
Vulnerability monitoring application using the [nvd.nist.gov](https://nvd.nist.gov/) API. Filters intervening vulnerabilities based on keywords used in the vulnerability description. \

The purpose of the application is to facilitate the process of monitoring vulnerabilities for various purposes. The application is free and can be used for commercial purposes. All license information is in the LICENSE file.

## Open Source
The full code for the application is available here on github, and you can build this on your server using Docker. The application is divided into two sections ``frontend`` in Vue and ``backend`` in FastApi.

If you are a person who would like to help improve the project then I look forward to hearing from you!

## Deployment
To deploy your application on the server you must have the following environment variables set:

```bash
export MYSQL_HOST = 'localhost'
export MYSQL_PORT = '3306'
export MYSQL_ROOT_PASSWORD = 'password'
export MYSQL_DB = 'dbName'
export MYSQL_USER = 'user'
export MYSQL_PASSWD = 'userpassword'
export BACKEND_URL = 'backend.localhost'
export SECRET = '$(openssl rand -hex 32)'
```

## Development
To run the application in development mode, just run the appropriate command. All environment variables are created dynamically.

```bash
chmod +x dev.sh
sudo dev.sh
```

After launching, your eyes will see logs from all docker instances. You can freely use ```CTRL + C``` to close them, it will not make the instances stop.

### Launch options
Running the script without specifying options, by default, deletes old docker instances and builds them anew. Additional options for running the development environment:
1. ```--stop``` - stops all docker instances.
2. ```--start``` - resumes stalled docker instances
3. ```--restart``` - restarts all docker instances

### Accounts
Two accounts are created in the development environment
1. ```admin:admin``` - administrator privileges
2. ```john:john``` - user permissions

Permission system:
```
0 == no permissions 
1 == normal permissions 
2 == Administrator
```

## Hints
Using the [vue-toastification](https://vue-toastification.maronato.dev/) library in file:
```javascript
import { useToast } from "vue-toastification";
const toast = useToast();
toast("Default toast");
toast.info("Info toast");
toast.success("Success toast");
toast.error("Error toast");
toast.warning("Warning toast");
```