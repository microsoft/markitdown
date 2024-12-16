class Markitdown < Formula
  desc "Markitdown: A tool for converting markdown documents"
  homepage "https://github.com/PratibhaK11/markitdown"
  url "https://github.com/PratibhaK11/markitdown/releases/download/v1.0.0-alpha/markitdown-1.0.0.tar.gz"
  sha256 "9f81ed1a9011545b4d4ad1318c61b0ab3c46230114036f0aed151c2b0e283c57"  # checksum

  depends_on "python@3.9"  # required Python version

  def install
    bin.install "dist/__main__" => "markitdown"  # Installing the binary
  end

  test do
    system "#{bin}/markitdown", "--help"
  end
end
