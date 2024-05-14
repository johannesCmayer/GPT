{ pkgs ? import <nixpkgs> {}, gsay }:

pkgs.python310Packages.buildPythonPackage rec {
  name = "gpt-ui";
  src = ./.;
  propagatedBuildInputs = with pkgs.python310Packages; [
    gsay.packages.x86_64-linux.default
    pkgs.python310
    pyyaml
    xdg-base-dirs
    rich
    google-cloud-texttospeech
  ];
}