Name:		jaf
Version:	1.2.1
Release:	5%{?dist}
Summary:	JavaBeans Activation Framework

License:	BSD
URL:		https://github.com/eclipse-ee4j/jaf

Source0:	https://github.com/eclipse-ee4j/jaf/archive/%{version}.tar.gz

BuildArch:	noarch
ExclusiveArch: x86_64

BuildRequires:	junit
BuildRequires:	maven-local
BuildRequires:	mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:	mvn(org.apache.maven.plugins:maven-dependency-plugin)
BuildRequires:	mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires:	mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:	mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:	mvn(org.commonjava.maven.plugins:directory-maven-plugin)
BuildRequires:	mvn(org.eclipse.ee4j:project:pom:)

%description
The JavaBeans Activation Framework (JAF) is a standard extension to the
Java platform that lets you take advantage of standard services to:
determine the type of an arbitrary piece of data; encapsulate access to it;
discover the operations available on it; and instantiate the appropriate
bean to perform the operation(s).

%package javadoc
Summary:	Javadoc for %{name}

%description javadoc
%{summary}.

%prep
%setup -q

%pom_disable_module demo

%pom_remove_plugin :maven-javadoc-plugin activation
%pom_remove_plugin :osgiversion-maven-plugin

# maven-dependency-plugin doesn't work correctly without access to remote repos
%pom_remove_plugin :maven-dependency-plugin activationapi
mkdir -p %{_builddir}/%{name}-%{version}/activationapi/target/sources/
cp -r %{_builddir}/%{name}-%{version}/activation/src/main/java/javax/ %{_builddir}/%{name}-%{version}/activationapi/target/sources/
%pom_xpath_inject "/pom:project"  "<dependencies>
<dependency>
  <groupId>com.sun.activation</groupId>
  <artifactId>jakarta.activation</artifactId>
  <version>1.2.1</version>
</dependency>
</dependencies>" "activationapi/pom.xml"

%build
%mvn_build -- -Dactivation.osgiversion=1.2.1

%install
%mvn_install

%files -f .mfiles
%license LICENSE.md
%license NOTICE.md
%doc README.md

%files javadoc -f .mfiles-javadoc
%license LICENSE.md
%license NOTICE.md
%doc README.md

%changelog
* Thu Mar 04 2021 Alex Macdonald <almacdon@redhat.com> - 1.2.1-5
- Add ExclusiveArch: x86_64

* Tue May 19 2020 Alex Macdonald <almacdon@redhat.com> - 1.2.1-4
- Add BuildRequires on junit

* Tue May 28 2019 Jie Kang <jkang@redhat.com> - 1.2.1-3
- Remove osgiversion-maven-plugin build requirement
- Remove javadoc plugin not needed in Fedora builds

* Thu Nov 22 2018 Salman Siddiqui <sasiddiq@redhat.com> - 1.2.1-2
- Use official version 1.2.1 release

* Fri Sep 21 2018 Salman Siddiqui <sasiddiq@redhat.com> - 1.2.1-1
- Initial packaging
