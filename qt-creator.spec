Summary:	An IDE tailored to the needs of Qt developers
Summary(pl.UTF-8):	IDE dostosowane do potrzeb developerow Qt
Name:		qt-creator
Version:	4.8.2
Release:	1
Epoch:		1
License:	LGPL v2.1
Group:		X11/Development/Tools
Source0:	http://download.qt.io/official_releases/qtcreator/4.8/%{version}/%{name}-opensource-src-%{version}.tar.xz
# Source0-md5:	bf5b9953cfec44aa2504e30cb81768e6
Patch0:		x32.patch
URL:		http://doc.qt.io/qt-5/topics-app-development.html
BuildRequires:	Qt5Concurrent-devel >= 5.9.0
BuildRequires:	Qt5Designer-devel >= 5.9.0
BuildRequires:	Qt5Gui-devel >= 5.9.0
BuildRequires:	Qt5Help-devel >= 5.9.0
BuildRequires:	Qt5Network-devel >= 5.9.0
BuildRequires:	Qt5Quick-controls >= 5.9.0
BuildRequires:	Qt5Quick-devel >= 5.9.0
BuildRequires:	Qt5Script-devel >= 5.9.0
BuildRequires:	Qt5Svg-devel >= 5.9.0
BuildRequires:	Qt5UiTools-devel >= 5.9.0
BuildRequires:	Qt5WebKit-devel >= 5.9.0
BuildRequires:	Qt5Xml-devel >= 5.9.0
BuildRequires:	clang-devel >= 6.0.0
BuildRequires:	gdb
BuildRequires:	libstdc++-devel
BuildRequires:	llvm-devel >= 6.0.0
BuildRequires:	qt5-build >= 5.9.0
BuildRequires:	qt5-linguist
BuildRequires:	qt5-qmake >= 5.9.0
BuildRequires:	rpmbuild(macros) >= 1.602
Requires(post,postun):	desktop-file-utils
%requires_eq	Qt5Core
Requires:	Qt5Gui-platform-xcb
Requires:	Qt5Quick-controls
Requires:	Qt5Sql-sqldriver-sqlite3
Requires:	hicolor-icon-theme
Requires:	qt5-qtdeclarative
# for xdg-open
Suggests:	xdg-utils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		skip_post_check_so	'libClangsupport\.so.*'

%description
Qt Creator is a cross-platform integrated development environment
(IDE) tailored to the needs of Qt developers.

%description -l pl.UTF-8
Qt Creator to wieloplatformowe IDE dostosowane do potrzeb developerow
Qt.

%prep
%setup -q -n %{name}-opensource-src-%{version}
%ifarch x32
%patch0 -p1
%endif

# fix unresolved symbols in libQtcSsh
echo >> src/libs/ssh/ssh_dependencies.pri
echo "LIBS += -ldl" >> src/libs/ssh/ssh_dependencies.pri

%build
export QTDIR=%{_libdir}/qt5
# the qmakespec in qt4 is somewhat broken, need to look at this
#export QMAKESPEC=%{_datadir}/qt4/mkspecs/linux-g++/

qmake-qt5 qtcreator.pro \
	IDE_LIBRARY_BASENAME="%{_lib}" \
	LLVM_INSTALL_DIR="%{_prefix}" \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_LINK="%{__cxx}" \
	QMAKE_CFLAGS_ISYSTEM=-I \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcxxflags}" \
	QMAKE_RPATH=

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_desktopdir}

export QTDIR=%{_libdir}/qt5
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT%{_prefix}

install -d $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/qtcreator" > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/qtcreator.conf

rm -f $RPM_BUILD_ROOT%{_libdir}/qtcreator/*.prl

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database
%update_icon_cache hicolor

%postun
/sbin/ldconfig
%update_desktop_database_postun
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qbs
%attr(755,root,root) %{_bindir}/qbs-config
%attr(755,root,root) %{_bindir}/qbs-config-ui
%attr(755,root,root) %{_bindir}/qbs-create-project
%attr(755,root,root) %{_bindir}/qbs-setup-android
%attr(755,root,root) %{_bindir}/qbs-setup-qt
%attr(755,root,root) %{_bindir}/qbs-setup-toolchains
%attr(755,root,root) %{_bindir}/qtcreator
%{_sysconfdir}/ld.so.conf.d/qtcreator.conf
%dir %{_libexecdir}/qtcreator
%attr(755,root,root) %{_libexecdir}/qtcreator/buildoutputparser
%attr(755,root,root) %{_libexecdir}/qtcreator/clangbackend
%attr(755,root,root) %{_libexecdir}/qtcreator/cpaster
%attr(755,root,root) %{_libexecdir}/qtcreator/dmgbuild
%attr(755,root,root) %{_libexecdir}/qtcreator/qbs_processlauncher
%attr(755,root,root) %{_libexecdir}/qtcreator/qml2puppet
%attr(755,root,root) %{_libexecdir}/qtcreator/qtcreator_process_stub
%attr(755,root,root) %{_libexecdir}/qtcreator/qtpromaker
%attr(755,root,root) %{_libexecdir}/qtcreator/sdktool
%dir %{_libdir}/qtcreator
%attr(755,root,root) %{_libdir}/qtcreator/lib*.so.*.*
%attr(755,root,root) %{_libdir}/qtcreator/lib*.so
%attr(755,root,root) %ghost %{_libdir}/qtcreator/lib*.so.1
%attr(755,root,root) %ghost %{_libdir}/qtcreator/lib*.so.4
%dir %{_libdir}/qtcreator/plugins
%attr(755,root,root) %{_libdir}/qtcreator/plugins/lib*.so
%dir %{_libdir}/qtcreator/plugins/qbs
%dir %{_libdir}/qtcreator/plugins/qbs/plugins
%attr(755,root,root) %{_libdir}/qtcreator/plugins/qbs/plugins/libclangcompilationdbgenerator.so
%attr(755,root,root) %{_libdir}/qtcreator/plugins/qbs/plugins/libmakefilegenerator.so
%attr(755,root,root) %{_libdir}/qtcreator/plugins/qbs/plugins/libqbs_cpp_scanner.so
%attr(755,root,root) %{_libdir}/qtcreator/plugins/qbs/plugins/libqbs_qt_scanner.so
%attr(755,root,root) %{_libdir}/qtcreator/plugins/qbs/plugins/libvisualstudiogenerator.so
%dir %{_libdir}/qtcreator/plugins/qmldesigner
%attr(755,root,root) %{_libdir}/qtcreator/plugins/qmldesigner/libcomponentsplugin.so
%attr(755,root,root) %{_libdir}/qtcreator/plugins/qmldesigner/libqtquickplugin.so
%{_datadir}/qtcreator
%{_datadir}/metainfo/org.qt-project.qtcreator.appdata.xml
%{_desktopdir}/org.qt-project.qtcreator.desktop
%{_iconsdir}/hicolor/*/*/*.png
