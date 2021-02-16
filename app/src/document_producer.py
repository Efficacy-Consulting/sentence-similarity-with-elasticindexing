# Import KafkaProducer from Kafka library
from kafka import KafkaProducer

# Import JSON module to serialize data
import json
from utils import print_with_time

topic_name = 'sentence-similarity'

# Initialize producer variable and set parameter for JSON encode
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         json.dumps(x).encode('utf-8'))

try:
  # Send data in JSON format
  producer.send(topic_name, {'id': '17287',
                            'title': 'Kim Jong-un Says North Korea Is Preparing to Test Long-Range Missile - The New York Times',
                            'publication': 'New York Times',
                            'sentence': 'SEOUL, South Korea  ‚Äî   North Korea‚Äôs leader, Kim   said on Sunday that his country was making final preparations to conduct its first test of an intercontinental ballistic missile  ‚Äî   a bold statement less than a month before the inauguration of   Donald J. Trump. Although North Korea has conducted five nuclear tests in the last decade and more than 20 ballistic missile tests in 2016 alone, and although it habitually threatens to attack the United States with nuclear weapons, the country has never   an intercontinental ballistic missile, or ICBM. In his annual New Year‚Äôs Day speech, which was broadcast on the North‚Äôs   KCTV on Sunday, Mr. Kim spoke proudly of the strides he said his country had made in its nuclear weapons and ballistic missile programs. He said North Korea would continue to bolster its weapons programs as long as the United States remained hostile and continued its joint military exercises with South Korea. ‚ÄúWe have reached the final stage in preparations to   an intercontinental ballistic rocket,‚Äù he said. Analysts in the region have said Mr. Kim might conduct another weapons test in coming months, taking advantage of leadership changes in the United States and South Korea. Mr. Trump will be sworn in on Jan. 20. In South Korea, President Park   whose powers were suspended in a Parliamentary impeachment on Dec. 9, is waiting for the Constitutional Court to rule on whether she should be formally removed from office or reinstated. If North Korea conducts a    test in coming months, it will test Mr. Trump‚Äôs new administration despite years of increasingly harsh sanctions, North Korea has been advancing toward Mr. Kim‚Äôs professed goal of arming his isolated country with the ability to deliver a nuclear warhead to the United States. Mr. Kim‚Äôs speech on Sunday indicated that North Korea may   a   rocket several times this year to complete its ICBM program, said Cheong   a senior research fellow at the Sejong Institute in South Korea. The first of such tests could come even before Mr. Trump‚Äôs inauguration, Mr. Cheong said. ‚ÄúWe need to take note of the fact that this is the first New Year‚Äôs speech where Kim   mentioned an intercontinental ballistic missile,‚Äù he said. In his speech, Mr. Kim did not comment on Mr. Trump‚Äôs election. Doubt still runs deep that North Korea has mastered all the technology needed to build a reliable ICBM. But analysts in the region said the North‚Äôs launchings of   rockets to put satellites into orbit in recent years showed that the country had cleared some key technological hurdles. After the North‚Äôs satellite launch in February, South Korean defense officials said the Unha rocket used in the launch, if successfully reconfigured as a missile, could fly more than 7, 400 miles with a warhead of 1, 100 to 1, 300 pounds  ‚Äî   far enough to reach most of the United States. North Korea has deployed Rodong ballistic missiles that can reach most of South Korea and Japan, but it has had a spotty record in   the Musudan, its   ballistic missile with a range long enough to reach American military bases in the Pacific, including those on Guam. The North has also claimed a series of successes in testing various ICBM technologies, although its claims cannot be verified and are often disputed by officials and analysts in the region. It has said it could now make nuclear warheads small enough to fit onto a ballistic missile. It also claimed success in testing the   technology that allows a   missile to return to the Earth‚Äôs atmosphere without breaking up. In April, North Korea reported the successful ground test of an engine for an intercontinental ballistic missile. At the time, Mr. Kim said the North ‚Äúcan tip   intercontinental ballistic rockets with more powerful nuclear warheads and keep any cesspool of evils in the Earth, including the U. S. mainland, within our striking range. ‚Äù On Sept. 9, the North conducted its fifth, and most powerful, nuclear test. Mr. Kim later attended another ground test of a new   rocket engine, exhorting his government to prepare for another rocket launch as soon as possible. In November, the United Nations Security Council imposed new  sanctions against the North.'
                            })
except Exception as e:
  print_with_time('Producer Send Error: ' + e)
finally:
  producer.close()

# Print message
print_with_time('Message Sent to: ' + topic_name)