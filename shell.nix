{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShellNoCC {
  packages = with pkgs; [
    python310
    python310Packages.openai
    python310Packages.prompt-toolkit
    python310Packages.tiktoken
    python310Packages.pyyaml
    python310Packages.xdg-base-dirs
    python310Packages.rich
  ];
}
