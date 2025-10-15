#
# Conditional build:
%bcond_with	tests		# build with tests
# TODO:
# PackageKit qt5
#
%define		kdeplasmaver	6.4.5
%define		qtver		5.15.2
%define		kpname		plasma-integration

Summary:	KDE Plasma Integration
Name:		kp6-%{kpname}
Version:	6.4.5
Release:	2
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	bb9f6a9cc4f43fa522ee77ece904f377
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Quick-devel >= %{qtver}
BuildRequires:	cmake >= 3.16.0
BuildRequires:	fontconfig-devel
BuildRequires:	kf6-attica-devel
BuildRequires:	kf6-kauth-devel
BuildRequires:	kf6-kcmutils-devel
BuildRequires:	kf6-kdbusaddons-devel
BuildRequires:	kf6-kdeclarative-devel
BuildRequires:	kf6-kdoctools-devel
BuildRequires:	kf6-kglobalaccel-devel
BuildRequires:	kf6-ki18n-devel
BuildRequires:	kf6-knewstuff-devel
BuildRequires:	kf6-knotifications-devel
BuildRequires:	kf6-knotifyconfig-devel
BuildRequires:	kf6-kpeople-devel
BuildRequires:	kf6-krunner-devel
BuildRequires:	kf6-kwallet-devel
BuildRequires:	kp6-breeze-devel
BuildRequires:	kp6-kwayland-devel
BuildRequires:	kp6-plasma-activities-stats-devel
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	xorg-driver-input-evdev-devel
BuildRequires:	xorg-driver-input-synaptics-devel
BuildRequires:	xorg-lib-libXft-devel
BuildRequires:	xz
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	kp5-%{kpname} < 6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
KDE Plasma Integration.

%package devel
Summary:	Header files for %{kpname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	kp5-%{kpname}-devel < 6

%description devel
Header files for %{kpname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kpname}.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DBUILD_QT5=OFF \
	-DBUILD_QT6=ON
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kpname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/qt6/plugins/platformthemes/KDEPlasmaPlatformTheme6.so
