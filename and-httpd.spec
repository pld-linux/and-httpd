# TODO
# - dedicated uid (or not?)
# - finish files after deps available

#
# Conditional build:
%bcond_without	tests		# build without tests

Summary:	Secure, simple and fast HTTP server
Name:		and-httpd
Version:	0.99.11
Release:	0.1
License:	LGPL
Group:		Daemons
URL:		http://www.and.org/and-httpd/
Source0:	http://www.and.org/and-httpd/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	c0775fa77dc72b4627205d83b2cd3f58
BuildRequires:	libcap-devel
BuildRequires:	perl-base
BuildRequires:	pkgconfig >= 0.8
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	socket_poll-devel
BuildRequires:	timer_q-devel
BuildRequires:	vstr-devel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Requires:	vstr >= 1.0.14
Provides:	user(http)
Provides:	webserver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		httpd_uid	51
%define		wwwdir	/home/services/httpd

%description
And-httpd is currently only a URL to file mapping daemon, in other
words in can take an incomming URL and map it to a file in a number of
ways. However it cannot do CGI or anything like apache-httpd
mod_python etc. ... it cannot even dynamically create directory
listings, however the -tools package contains utilities that can do
them outside of the daemon.

%package tools
Summary:	Tools to help with managing webserver data
Group:		Development/Tools
Requires:	perl-base
Requires:	python
Requires:	scons

%description tools
Tools to help managing data under /var/www, including:
- automatic directory indexer.
- automatic gzip encoding generator.
- automatic converter from and-httpd syslog to Apache-httpd combined
  log.

%prep
%setup -q

%build
%configure \
	%{?debug:--enable-debug} \
	%{?debug:--enable-debug-vstr} \
	%{?debug:--enable-debug-timer_q} \
	%{nil}

%{__make} %{?with_tests:check}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%if 0
%pre
%useradd -c "And-httpd" -u %{httpd_uid} -s /sbin/nologin -r -d %{wwwdir} and-httpd

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi
%endif

%files
%defattr(644,root,root,755)
%doc %{_datadir}/doc/and-httpd-*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_bindir}/*
%{_sysconfdir}/and-httpd/conf.d/README
%attr(754,root,root) /etc/rc.d/init.d/and-httpd
%{_sysconfdir}/cron.hourly/and-httpd_*
%config(noreplace) %{_sysconfdir}/and-httpd/and-httpd.conf
%config(noreplace) %{_sysconfdir}/and-httpd/conf.d/_*.conf
%config %{_sysconfdir}/and-httpd/mime_types_extra.txt
%{wwwdir}/err/*
%{wwwdir}/conf/*
%{wwwdir}/conf_tmpl/*
%{wwwdir}/html
%{wwwdir}/generated_html
%{_mandir}/man8/and-httpd*
%{_mandir}/man5/and-httpd*

%files tools
%defattr(644,root,root,755)
%{_datadir}/and-httpd-*-tools/*
%{_libexecdir}/and-httpd-*-tools/*
