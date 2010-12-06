%define name	nmis
%define version 2.00
%define up_version %(echo %version | sed -e 's/\\./-/')
%define release %mkrel 4

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Network Management Information System
License:	GPL
Group:		Networking/WWW
URL:		http://nmis.sourceforge.net/
Source:     http://www.sins.com.au/public/%{name}-%{up_version}.tar.gz
Patch0:     %{name}-2.00-fhs.patch
Patch1:     %{name}-2.00-no-ksh.patch
%if %mdkversion < 201010
Requires(post):   rpm-helper
Requires(postun):   rpm-helper
%endif
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
NMIS stands for Network Management Information System.  It is a Network
Management System which performs multiple functions from the OSI Network
Management Functional Areas, those being, Performance, Configuration, Fault.

%prep
%setup -q -n %{name}-%{up_version}
%patch0 -p1
%patch1 -p1

%build

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_var}/www/%{name}
install -m 755 cgi-bin/* %{buildroot}%{_var}/www/%{name}

install -d -m 755 %{buildroot}%{_datadir}/%{name}/lib
install -m 644 lib/* %{buildroot}%{_datadir}/%{name}/lib

install -d -m 755 %{buildroot}%{_datadir}/%{name}/bin
install -m 755 bin/* %{buildroot}%{_datadir}/%{name}/bin

install -d -m 755 %{buildroot}%{_datadir}/%{name}/mibs
install -m 644 mibs/* %{buildroot}%{_datadir}/%{name}/bin

install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
install -m 644 conf/nmis-sample.conf \
    %{buildroot}%{_sysconfdir}/%{name}/nmis.conf
install -m 644 conf/nodes-sample.csv \
    %{buildroot}%{_sysconfdir}/%{name}/nodes.csv
install -m 644 conf/locations-sample.csv \
    %{buildroot}%{_sysconfdir}/%{name}/locations.csv
install -m 644 conf/contacts-sample.csv \
    %{buildroot}%{_sysconfdir}/%{name}/contacts.csv

install -d -m 755 %{buildroot}%{_var}/lib/%{name}
install -d -m 755 %{buildroot}%{_var}/log/%{name}

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# %{name} Apache configuration
Alias /%{name} %{_var}/www/%{name}

<Directory %{_var}/www/%{name}>
    Order allow,deny
    Allow from all
    Options ExecCGI
    AddHandler cgi-script .pl
    DirectoryIndex nmiscgi.pl
</Directory>
EOF

%clean
rm -rf %{buildroot}

%post
%if %mdkversion < 201010
%_post_webapp
%endif

%postun
%if %mdkversion < 201010
%_postun_webapp
%endif

%files
%defattr(-,root,root)
%doc README gpl.txt changes.txt htdocs/*
%config(noreplace) %{_webappconfdir}/%{name}.conf
%{_var}/www/%{name}
%{_var}/lib/%{name}
%{_var}/log/%{name}
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}

