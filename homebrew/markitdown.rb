class Markitdown < Formula
  desc "Python tool for converting files and office documents to Markdown"
  homepage "https://github.com/microsoft/markitdown"
  version "0.1.4" # Update this on new releases
  license "MIT"

  if OS.mac? && Hardware::CPU.intel?
    url "https://github.com/microsoft/markitdown/releases/download/v#{version}/markitdown-macos-x64"
    sha256 "REPLACE_WITH_REAL_SHA256_WHEN_RELEASED"
  elsif OS.mac? && Hardware::CPU.arm?
    # For now, using x64 binary on ARM via Rosetta until we add ARM runners to CI
    url "https://github.com/microsoft/markitdown/releases/download/v#{version}/markitdown-macos-x64"
    sha256 "REPLACE_WITH_REAL_SHA256_WHEN_RELEASED"
  elsif OS.linux? && Hardware::CPU.intel?
    url "https://github.com/microsoft/markitdown/releases/download/v#{version}/markitdown-linux-x64"
    sha256 "REPLACE_WITH_REAL_SHA256_WHEN_RELEASED"
  end

  def install
    bin.install "markitdown-macos-x64" => "markitdown" if OS.mac?
    bin.install "markitdown-linux-x64" => "markitdown" if OS.linux?
  end

  test do
    system "#{bin}/markitdown", "--version"
  end
end
