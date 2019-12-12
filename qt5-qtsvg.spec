#
# Conditional build:
%bcond_without	doc	# Documentation

%define		orgname		qtsvg
%define		qtbase_ver	%{version}
%define		qttools_ver	%{version}
Summary:	The Qt5 Svg library
Summary(pl.UTF-8):	Biblioteka Qt5 Svg
Name:		qt5-%{orgname}
Version:	5.14.0
Release:	1
License:	LGPL v2.1 with Digia Qt LGPL Exception v1.1 or GPL v3.0
Group:		X11/Libraries
Source0:	http://download.qt.io/official_releases/qt/5.14/%{version}/submodules/%{orgname}-everywhere-src-%{version}.tar.xz
# Source0-md5:	48ccf81077499a09edf06a7487350df1
URL:		http://www.qt.io/
BuildRequires:	Qt5Core-devel >= %{qtbase_ver}
BuildRequires:	Qt5Gui-devel >= %{qtbase_ver}
BuildRequires:	Qt5OpenGL-devel >= %{qtbase_ver}
BuildRequires:	Qt5Widgets-devel >= %{qtbase_ver}
BuildRequires:	Qt5Xml-devel >= %{qtbase_ver}
%if %{with doc}
BuildRequires:	qt5-assistant >= %{qttools_ver}
%endif
BuildRequires:	qt5-build >= %{qtbase_ver}
BuildRequires:	qt5-qmake >= %{qtbase_ver}
BuildRequires:	rpmbuild(macros) >= 1.654
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing
%define		qt5dir		%{_libdir}/qt5

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

This package contains Qt5 Svg library.

%description -l pl.UTF-8
Qt to wieloplatformowy szkielet aplikacji i interfejsów użytkownika.
Przy użyciu Qt można pisać aplikacje powiązane z WWW i wdrażać je w
systemach biurkowych, przenośnych i wbudowanych bez przepisywania kodu
źródłowego.

Ten pakiet zawiera bibliotekę Qt5 Svg.

%package -n Qt5Svg
Summary:	The Qt5 Svg library
Summary(pl.UTF-8):	Biblioteka Qt5 Svg
Group:		Libraries
Requires:	Qt5Core >= %{qtbase_ver}
Requires:	Qt5Gui >= %{qtbase_ver}
Requires:	Qt5Widgets >= %{qtbase_ver}
Obsoletes:	qt5-qtsvg

%description -n Qt5Svg
Qt5 Svg library provides functionality for handling SVG images.

%description -n Qt5Svg -l pl.UTF-8
Biblioteka Qt5 Svg udostępnia obsługę obrazów SVG.

%package -n Qt5Svg-devel
Summary:	Qt5 Svg library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 Svg - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	OpenGL-devel
Requires:	Qt5Core-devel >= %{qtbase_ver}
Requires:	Qt5Gui-devel >= %{qtbase_ver}
Requires:	Qt5Svg = %{version}-%{release}
Requires:	Qt5Widgets-devel >= %{qtbase_ver}
Requires:	zlib-devel
Obsoletes:	qt5-qtsvg-devel

%description -n Qt5Svg-devel
Qt5 Svg library - development files.

%description -n Qt5Svg-devel -l pl.UTF-8
Biblioteka Qt5 Svg - pliki programistyczne.

%package doc
Summary:	Qt5 Svg documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Svg w formacie HTML
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
Qt5 Svg documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Svg w formacie HTML.

%package doc-qch
Summary:	Qt5 Svg documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Svg w formacie QCH
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc-qch
Qt5 Svg documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Svg w formacie QCH.

%package examples
Summary:	Qt5 Svg examples
Summary(pl.UTF-8):	Przykłady do biblioteki Qt5 Svg
Group:		X11/Development/Libraries
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description examples
Qt5 Svg examples.

%description examples -l pl.UTF-8
Przykłady do biblioteki Qt5 Svg.

%prep
%setup -q -n %{orgname}-everywhere-src-%{version}

%build
qmake-qt5
%{__make}
%{?with_doc:%{__make} docs}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{with doc}
%{__make} install_docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# useless symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.so.5.??
# actually drop *.la, follow policy of not packaging them when *.pc exist
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.la

# Prepare some files list
ifecho() {
	r="$RPM_BUILD_ROOT$2"
	if [ -d "$r" ]; then
		echo "%%dir $2" >> $1.files
	elif [ -x "$r" ] ; then
		echo "%%attr(755,root,root) $2" >> $1.files
	elif [ -f "$r" ]; then
		echo "$2" >> $1.files
	else
		echo "Error generation $1 files list!"
		echo "$r: no such file or directory!"
		return 1
	fi
}
ifecho_tree() {
	ifecho $1 $2
	for f in `find $RPM_BUILD_ROOT$2 -printf "%%P "`; do
		ifecho $1 $2/$f
	done
}

echo "%defattr(644,root,root,755)" > examples.files
ifecho_tree examples %{_examplesdir}/qt5/svg

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt5Svg -p /sbin/ldconfig
%postun	-n Qt5Svg -p /sbin/ldconfig

%files -n Qt5Svg
%defattr(644,root,root,755)
%doc dist/changes-*
%attr(755,root,root) %{_libdir}/libQt5Svg.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Svg.so.5
%attr(755,root,root) %{qt5dir}/plugins/iconengines/libqsvgicon.so
%attr(755,root,root) %{qt5dir}/plugins/imageformats/libqsvg.so

%files -n Qt5Svg-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Svg.so
%{_libdir}/libQt5Svg.prl
%{_includedir}/qt5/QtSvg
%{_pkgconfigdir}/Qt5Svg.pc
%dir %{_libdir}/cmake/Qt5Svg
%{_libdir}/cmake/Qt5Svg/Qt5SvgConfig*.cmake
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QSvgIconPlugin.cmake
%{_libdir}/cmake/Qt5Gui/Qt5Gui_QSvgPlugin.cmake
%{qt5dir}/mkspecs/modules/qt_lib_svg.pri
%{qt5dir}/mkspecs/modules/qt_lib_svg_private.pri

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtsvg

%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtsvg.qch
%endif

%files examples -f examples.files
%defattr(644,root,root,755)
# XXX: dir shared with qt5-qtbase-examples
%dir %{_examplesdir}/qt5
