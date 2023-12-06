## Deploying
Manual (remember to setup env vars):
```bash
chmod +x run.sh && ./run.sh
```
After push to main this is automated

## Deploying requirements
Docker >= 4.20

Environment variables:
```bash
export MYSQL_HOST = ''
export MYSQL_PORT = ''
export MYSQL_ROOT_PASSWORD = ''
export MYSQL_DB = ''
export MYSQL_USER = ''
export MYSQL_PASSWD = ''
export BACKEND_URL = ''
export SECRET = ''
```

## Development
In development process all environment variables are created dynamically. You just need have installed docker, run as root ```dev.sh``` in your **linux** terminal.

```bash
chmod +x dev.sh && sudo ./dev.sh
```
#### Restarting
```bash
sudo ./dev.sh --restart
```

#### Stopping
```bash
sudo ./dev.sh --stop
```
### Credentials
```python
username = 'admin'
password = 'admin'
permissions = 2

username = 'john'
password = 'john'
permissions = 1
```

## Using toast
```javascript
import { useToast } from "vue-toastification";
const toast = useToast();
toast("Default toast");
toast.info("Info toast");
toast.success("Success toast");
toast.error("Error toast");
toast.warning("Warning toast");
```