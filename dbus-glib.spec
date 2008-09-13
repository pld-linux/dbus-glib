#
# Conditional build:
%bcond_without	apidocs         # disable gtk-doc
%bcond_without	static_libs	# don't build static library
#
%define		dbus_version	0.93
%define		expat_version	1:1.95.5
%define		glib_version	1:2.10.1
#
Summary:	GLib-based library for using D-BUS
Summary(pl.UTF-8):	Biblioteka do używania D-BUS oparta o GLib
Name:		dbus-glib
Version:	0.76
Release:	1
License:	AFL v2.1 or GPL v2
Group:		Libraries
Source0:	http://dbus.freedesktop.org/releases/dbus-glib/%{name}-%{version}.tar.gz
# Source0-md5:	d3b716a7e798faa1c6a867675f00306a
Source1:	dbus-bus-introspect.xml
Patch0:		%{name}-configure.patch
Patch1:		%{name}-nolibs.patch
URL:		http://www.freedesktop.org/Software/DBusBindings
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-devel >= %{dbus_version}
BuildRequires:	expat-devel >= %{expat_version}
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= %{glib_version}
%{?with_apidocs:BuildRequires:	gtk-doc-automake >= 1.8}
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.98
Requires:	dbus-libs >= %{dbus_version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
D-BUS add-on library to integrate the standard D-BUS library with the
GLib thread abstraction and main loop.

%description -l pl.UTF-8
Dodatkowa biblioteka D-BUS do integracji standardowej biblioteki D-BUS
z abstrakcją wątków i główną pętlą GLib.

%package devel
Summary:	Header files for GLib-based library for using D-BUS
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki do używania D-BUS opartej o GLib
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	dbus-devel >= %{dbus_version}
Requires:	glib2-devel >= %{glib2_version}

%description devel
Header files for GLib-based library for using D-BUS.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki do używania D-BUS opartej o GLib.

%package static
Summary:	Static GLib-based library for using D-BUS
Summary(pl.UTF-8):	Statyczna biblioteka do używania D-BUS oparta o GLib
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GLib-based library for using D-BUS.

%description static -l pl.UTF-8
Statyczna biblioteka do używania D-BUS oparta o GLib.

%package apidocs
Summary:	D-BUS-GLib API documentation
Summary(pl.UTF-8):	Dokumentacja API D-BUS-GLib
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
D-BUS-GLib API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API D-BUS-GLib.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%if !%{with apidocs}
echo 'EXTRA_DIST=' > gtk-doc.make
echo 'AC_DEFUN([GTK_DOC_CHECK],[])' >> acinclude.m4
%endif

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_apidocs:--disable-gtk-doc} \
	%{?with_apidocs:--with-html-dir=%{_gtkdocdir}} \
	%{!?with_static_libs:--disable-static} \
	--with-xml=expat

cp %{SOURCE1} tools

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
# AFL not in common-licenses, so COPYING included
%doc AUTHORS COPYING ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libdbus-glib-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdbus-glib-1.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dbus-binding-tool
%attr(755,root,root) %{_libdir}/libdbus-glib-1.so
%{_libdir}/libdbus-glib-1.la
%{_includedir}/dbus*/dbus/dbus-glib*.h
%{_includedir}/dbus*/dbus/dbus-gtype-specialized.h
%{_pkgconfigdir}/dbus-glib-1.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libdbus-glib-1.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/dbus-glib
%endif
