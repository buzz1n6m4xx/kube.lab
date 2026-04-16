<?php
$servers = new Datastore();
$servers->newServer('ldap_pla');

// LDAP server hostname (Docker service name!)
$servers->setValue('server','host','openldap');
$servers->setValue('server','port',389);

// Base DN for your directory
$servers->setValue('server','base',array('dc=kube,dc=lab'));
$servers->setValue('server','name','OpenLDAP - kube.lab');

// Login settings
$servers->setValue('login','auth_type','session');
$servers->setValue('login','bind_id','cn=admin,dc=kube,dc=lab');
?>
