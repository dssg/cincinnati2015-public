## What is this?

This is a simple webapp we used to compare different models. Webapp reads in a directory of pickle files (as 
produced by our modeling code), shows an overview of the different models and allows to look at detailed
evaluations of each model

By default the webapp looks for pickle files in the `results` folder. This can be changed in `webapp/ioutils.py`.

## To run with the flask development server

    python run_webapp.py
    
## To deploy properly using gunicorn and nginx    

### Start gunicorn

    gunicorn -w 4 -b 127.0.0.1:4000 webapp:app &
    
#### nginx config file

    server {
        listen 80;
        access_log  /var/log/nginx/example.log;
    
        auth_basic "Restricted";
        auth_basic_user_file /etc/htpasswd/.cincy_htpasswd;
    
        location / {
            proxy_pass http://127.0.0.1:4000;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
    
#### restart nginx
    
     sudo service nginx restart


