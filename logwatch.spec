%include	/usr/lib/rpm/macros.perl
Summary:	Analyzes system logs
Summary(pl):	Logwatch - analizator log�w systemowych
Name:		logwatch
Version:	7.0
Release:	1
License:	MIT
Group:		Applications/System
# Path for stable versions:
Source0:	ftp://ftp.logwatch.org/pub/linux/%{name}-%{version}.tar.gz
# Source0-md5:	58fc1ea61df69e0e0839e70a289f5b3e
# Path for pre-versions:
#Source0:	ftp://ftp.kaybee.org/pub/beta/linux/%{name}-pre%{version}.tar.gz
Source1:	%{name}.cron
Source2:	%{name}.sysconfig
Patch0:		%{name}-log_conf.patch
URL:		http://www.logwatch.org/
BuildRequires:	rpm-perlprov
Requires:	crondaemon
Requires:	gawk
Requires:	perl-modules
Requires:	smtpdaemon
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_logwatchdir	%{_datadir}/%{name}
%define		_logwatchconf	%{_sysconfdir}/%{name}

%description
LogWatch is a customizable, pluggable log-monitoring system. It will
go through your logs for a given period of time and make a report in
the areas that you wish with the detail that you wish. Easy to use -
works right out of the package on almost all systems.

%description -l pl
Pakiet zawiera logwatch - program przeznaczony do automatycznego
analizowania log�w systemowych i przesy�aniu ich po wst�pnej obr�bce
poczt� elektroniczn� do administratora systemu. Logwatch jest �atwy w
u�yciu i mo�e pracowa� na wi�kszo�ci system�w.

%prep
%setup -q
%patch0 -p1

find -name '*~' | xargs -r rm

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_logwatchconf}/{conf,scripts},/etc/{cron.daily,sysconfig}} \
	$RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,%{_logwatchdir}/{lib,default.conf},/var/cache/logwatch}

install conf/logwatch.conf $RPM_BUILD_ROOT%{_logwatchconf}/conf
install conf/logwatch.conf $RPM_BUILD_ROOT%{_logwatchdir}/default.conf
# Where to put it The Right Way(TM)?
install lib/Logwatch.pm $RPM_BUILD_ROOT%{_logwatchdir}/lib

cp -a conf/services $RPM_BUILD_ROOT%{_logwatchconf}/conf
cp -a conf/services $RPM_BUILD_ROOT%{_logwatchdir}/default.conf
cp -a conf/logfiles $RPM_BUILD_ROOT%{_logwatchconf}/conf
cp -a conf/logfiles $RPM_BUILD_ROOT%{_logwatchdir}/default.conf
cp -a scripts $RPM_BUILD_ROOT%{_logwatchdir}

mv $RPM_BUILD_ROOT%{_logwatchdir}/scripts/logwatch.pl $RPM_BUILD_ROOT%{_sbindir}/logwatch

ln -sf %{_sbindir}/logwatch $RPM_BUILD_ROOT%{_logwatchdir}/scripts/logwatch.pl

install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.daily/00-%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

install logwatch.8 $RPM_BUILD_ROOT%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# needed for smooth upgrade from < 4.3.2 package
if [ -d /etc/log.d/conf ]; then
	mv -f /etc/log.d/conf/logwatch.conf* /etc/log.d/
	mv -f /etc/log.d/conf/services /etc/log.d/
	mv -f /etc/log.d/conf/logfiles /etc/log.d/
# needed for smooth upgrade from < 7.0 package:
elif [ -d /etc/log.d ]; then
	echo "Moving configuration from /etc/log.d to /etc/logwatch/conf..."
	mkdir -p /etc/logwatch/conf
#	mkdir /etc/logwatch/conf/logfiles
#	mkdir /etc/logwatch/conf/services
	mv -f /etc/log.d/logwatch.conf* /etc/logwatch/conf/
	mv -f /etc/log.d/services /etc/logwatch/conf/
	mv -f /etc/log.d/logfiles /etc/logwatch/conf/
fi

%files
%defattr(644,root,root,755)
%doc README HOWTO-* project/{CHANGES,TODO}
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/%{name}
%attr(755,root,root) /etc/cron.daily/00-%{name}
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_logwatchconf}/conf/logwatch.conf
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_logwatchconf}/conf/logfiles/*.conf
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_logwatchconf}/conf/services/*.conf
%attr(750,root,root) %dir %{_logwatchconf}
%attr(750,root,root) %dir %{_logwatchconf}/conf/logfiles
%attr(750,root,root) %dir %{_logwatchconf}/conf/services
%attr(750,root,root) %dir %{_logwatchconf}/scripts
%attr(755,root,root) %{_logwatchdir}
%attr(755,root,root) %{_sbindir}/logwatch
%attr(750,root,root) %dir /var/cache/logwatch
%{_mandir}/man8/*
