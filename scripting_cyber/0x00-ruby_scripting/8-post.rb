#!/usr/bin/env ruby
require 'net/http'
require 'uri'
require 'json'

def post_request(url, body_params = {})
  uri = URI.parse(url)

  # Create an HTTP POST request
  request = Net::HTTP::Post.new(uri)
  request.content_type = 'application/json'
  request.body = body_params.to_json unless body_params.empty?

  # Initialize the HTTP session
  response = Net::HTTP.start(uri.hostname, uri.port, use_ssl: uri.scheme == 'https') do |http|
    http.request(request)
  end

  # Print response status and body
  puts "Response status: #{response.code} #{response.message}"
  puts "Response body:"
  puts JSON.pretty_generate(JSON.parse(response.body))
end
