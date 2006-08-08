#
%define		dbus_version	0.91
%define		expat_version	1:1.95.5
%define		glib_version	1:2.10.1
#
Summary:	GLib-based library for using D-BUS
Summary(pl):	Biblioteka do u¿ywania D-BUS oparta o GLib
Name:		dbus-glib
Version:	0.71
Release:	1
License:	AFL v2.1 or GPL v2
Group:		Libraries
Source0:	http://dbus.freedesktop.org/releases/%{name}-%{version}.tar.gz
# Source0-md5:	4e1e7348b26ee8b6485452113f4221cc
URL:		http://www.freedesktop.org/Software/dbus
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	dbus-devel >= %{dbus_version}
BuildRequires:	expat-devel >= %{expat_version}
BuildRequires:	glib2-devel >= %{glib_version}
BuildRequires:	pkgconfig
Requires:	dbus-libs >= %{dbus_version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
D-BUS add-on library to integrate the standard D-BUS library with the
GLib thread abstraction and main loop.

%description -l pl
Dodatkowa biblioteka D-BUS do integracji standardowej biblioteki D-BUS
z abstrakcj± w±tków i g³ówn± pêtl± GLib.

%package devel
Summary:	Header files for GLib-based library for using D-BUS
Summary(pl):	Pliki nag³ówkowe biblioteki do u¿ywania D-BUS opartej o GLib
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	dbus-devel >= %{dbus_version}
Requires:	glib2-devel >= %{glib2_version}

%description devel
Header files for GLib-based library for using D-BUS.

%description devel -l pl
Pliki nag³ówkowe biblioteki do u¿ywania D-BUS opartej o GLib.

%package static
Summary:	Static GLib-based library for using D-BUS
Summary(pl):	Statyczna biblioteka do u¿ywania D-BUS oparta o GLib
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GLib-based library for using D-BUS.

%description static -l pl
Statyczna biblioteka do u¿ywania D-BUS oparta o GLib.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-xml=expat
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdbus-glib-1.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dbus-binding-tool
%attr(755,root,root) %{_libdir}/libdbus-glib-1.so
%{_libdir}/libdbus-glib-1.la
%{_includedir}/dbus*/dbus/dbus-glib*.h
%{_includedir}/dbus*/dbus/dbus-gtype-specialized.h
%{_pkgconfigdir}/dbus-glib-1.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libdbus-glib-1.a
