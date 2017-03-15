# shorty
Url shortener

### Requirements
- Docker
- Docker Compose

### Configuration
`cp app/config/.env.default app/config/.env` - copy config<br/>
`nano app/config/.env` - fill out secrets

### Usage
`docker-compose build && docker-compose up` - than visit localhost:9000

### Additional
Admin view for model overview is available under localhost:9000/admin<br/>
Unfortunately requires no auth yet

### ToDo
- Secure admin panel
- Add any frontend framework
- Style the pages
- Start hosting the project and get rich
