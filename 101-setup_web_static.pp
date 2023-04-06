# File: 101-setup_web_static.pp

class setup_web_static {
  package { 'nginx':
    ensure => installed,
  }

  file { '/data':
    ensure => directory,
    owner  => 'ubuntu',
    group  => 'ubuntu',
  }

  file { '/data/web_static':
    ensure => directory,
    owner  => 'ubuntu',
    group  => 'ubuntu',
  }

  file { '/data/web_static/releases':
    ensure => directory,
    owner  => 'ubuntu',
    group  => 'ubuntu',
  }

  file { '/data/web_static/shared':
    ensure => directory,
    owner  => 'ubuntu',
    group  => 'ubuntu',
  }

  file { '/data/web_static/releases/test':
    ensure => directory,
    owner  => 'ubuntu',
    group  => 'ubuntu',
  }

  file { '/data/web_static/releases/test/index.html':
    ensure => file,
    owner  => 'ubuntu',
    group  => 'ubuntu',
    content => 'Hello World',
  }

  file { '/data/web_static/current':
    ensure => 'link',
    target => '/data/web_static/releases/test',
    owner  => 'ubuntu',
    group  => 'ubuntu',
    require => File['/data/web_static/releases/test'],
  }

  file { '/etc/nginx/sites-available/default':
    ensure => file,
    owner  => 'root',
    group  => 'root',
    content => "
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 http://cuberule.com/;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}
",
    require => Package['nginx'],
  }

  service { 'nginx':
    ensure => 'running',
    enable => true,
    require => File['/etc/nginx/sites-available/default'],
  }
}

include setup_web_static

