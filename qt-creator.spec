Summary:	An IDE tailored to the needs of Qt developers
Summary(pl.UTF-8):	IDE dostosowane do potrzeb developerow Qt
Name:		qt-creator
Version:	1.3.1
Release:	3
Epoch:		1
License:	LGPL v2.1
Group:		X11/Development/Tools
Source0:	http://download.qtsoftware.com/qtcreator/%{name}-%{version}-src.zip
# Source0-md5:	b4c66810c591f62aa26739f997ffe88b
Source1:	%{name}.desktop
Patch0:		%{name}-pluginpath64.patch
URL:		http://www.qtsoftware.com/developer/qt-creator
BuildRequires:	QtDBus-devel
BuildRequires:	QtDesigner-devel
BuildRequires:	QtGui-devel
BuildRequires:	QtHelp-devel
BuildRequires:	QtNetwork-devel
BuildRequires:	QtScript-devel
BuildRequires:	QtSql-sqlite3
BuildRequires:	QtSvg-devel
BuildRequires:	QtWebKit-devel
BuildRequires:	QtXml-devel
BuildRequires:	qt4-build >= 4.6.0
BuildRequires:	qt4-linguist
BuildRequires:	qt4-qmake >= 4.6.0
BuildRequires:	unzip
Requires(post,postun):	desktop-file-utils
%requires_eq	QtCore
Requires:	QtSql-sqlite3
# for xdg-open
Suggests:	xdg-utils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Qt Creator is a cross-platform integrated development environment (IDE) 
tailored to the needs of Qt developers.

%description -l pl.UTF-8
Qt Creator to wieloplatformowe IDE dostosowane do potrzeb developerow Qt.

%prep
%setup -q -n %{name}-%{version}-src

%if "%{_lib}" == "lib64"
%patch0 -p1
%endif

%build
export QTDIR=%{_libdir}/qt4
# the qmakespec in qt4 is somewhat broken, need to look at this
#export QMAKESPEC=%{_datadir}/qt4/mkspecs/linux-g++/

qmake-qt4 qtcreator.pro \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_LINK="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcflags}" \
	QMAKE_RPATH=	

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_desktopdir}

export QTDIR=%{_libdir}/qt4
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT%{_prefix}

%if "%{_lib}" == "lib64"
mv -f $RPM_BUILD_ROOT{%{_prefix}/lib,%{_libdir}}
%endif

mv -f $RPM_BUILD_ROOT%{_bindir}/{qtcreator.bin,qtcreator}

install -d $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/qtcreator" > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/qtcreator.conf

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database

%postun
/sbin/ldconfig
%update_desktop_database_postun

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qtcreator
%attr(755,root,root) %{_bindir}/qtcreator_process_stub
%{_sysconfdir}/ld.so.conf.d/qtcreator.conf
%dir %{_libdir}/qtcreator
%attr(755,root,root) %{_libdir}/qtcreator/lib*.so.*.*
%attr(755,root,root) %{_libdir}/qtcreator/lib*.so
%attr(755,root,root) %ghost %{_libdir}/qtcreator/lib*.so.1
%dir %{_libdir}/qtcreator/plugins
%dir %{_libdir}/qtcreator/plugins/Nokia
%{_libdir}/qtcreator/plugins/Nokia/*.pluginspec
%attr(755,root,root) %{_libdir}/qtcreator/plugins/Nokia/*.so
%{_datadir}/qtcreator
%{_defaultdocdir}/qtcreator
%{_desktopdir}/qt-creator.desktop
%{_pixmapsdir}/qtcreator_logo*.png
