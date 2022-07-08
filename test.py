import unittest
import Handbook
import pandas as pd

class HandBook(unittest.TestCase):

  def test_videoID(self):
    result = Handbook.get_video_id('https://www.youtube.com/watch?v=hQoKX5kAonw')
    self.assertEqual(result,'hQoKX5kAonw')

  def test_dictonaries(self):
    
    result = Handbook.videos_related_to('hQoKX5kAonw')
    self.assertEqual(type(result), type({}))

    result = Handbook.videos_by_search_word('cars')
    self.assertEqual(type(result), type({}))

    result = Handbook.get_most_popular_videos()
    self.assertEqual(type(result),type({}))

  def test_data_frame(self):
    df = Handbook.create_topic_dataframe()
    self.assertEqual(type(df), pd.DataFrame) #this one might not work because you need user input, but we shall see

    df = Handbook.create_popular_dataframe()
    self.assertEqual(type(df), pd.DataFrame)

    df = Handbook.create_relate_to_dataframe()
    self.assertEqual(type(df), pd.DataFrame)


if __name__ == '__main__':
  unittest.main()