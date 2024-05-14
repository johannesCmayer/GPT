{ pkgs ? import <nixpkgs> {}, gsay }:

pkgs.python310Packages.buildPythonPackage rec {
  name = "gsay";
  src = ./.;
  propagatedBuildInputs = with pkgs.python310Packages; [
    pkgs.python310
    pyyaml
    xdg-base-dirs
    rich
    google-cloud-texttospeech
  ];
}