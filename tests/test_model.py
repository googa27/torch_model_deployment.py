import unittest
import torch
from inference import ts  # Import the loaded model

class TestModel(unittest.TestCase):
    '''
    Unit tests for the doubleit model.
    '''
    def test_doubleit(self):
        '''
        Test that the model correctly doubles the input tensor.
        '''
        sample_tensor = torch.tensor([1, 2, 3, 4])
        expected_output = torch.tensor([2, 4, 6, 8])
        result = ts(sample_tensor)
        self.assertTrue(torch.equal(result, expected_output))

if __name__ == '__main__':
    unittest.main()