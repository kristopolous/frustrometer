
require 'rubygems'
require 'bundler'
Bundler.require

# This is what will be emitted to the screen
parsed = {:idList => []}

File.open('7748857', 'r') { | content |
  raw = content.read
  doc = Nokogiri::HTML(raw, &:noblanks)

# This is the top link set
  linkContainer = doc.css('.comhead').first

# This may be a link to the parent
  last = linkContainer.css('a').last
  
# This means we should go to the parent
  if last.inner_html == 'parent'
    parsed[:parent] = last.attr('href').split('=').pop.to_i
  end

# We also need to note all the item ids we see here.
  doc.css('.comhead').map { | x |
  # The second item is the link
    link = x.css('a')[1]

    if link.inner_html != "link"
      raise "The link should be called 'link'. Aborting"
    end

    parsed[:idList] << link.attr('href').split('=').pop.to_i 
  }
}

puts parsed.to_json
