import unittest

import numpy as np

from gym import envs
from gym import spaces
import gym_oscillator


class TestAPIMethods(unittest.TestCase):

    def setUp(self):
        np.random.seed(0)
        self.env = envs.make('oscillator-v0')

    def tearDown(self):
        pass

    def test_spaces(self):
        self.assertEqual(self.env.action_space.n, 9)
        self.assertIsInstance(self.env.action_space, spaces.discrete.Discrete)
        # print(self.env.observation_space)
        self.assertIsInstance(self.env.observation_space, spaces.box.Box)

    def test_api_methods(self):
        observation, reward, done, d = self.env.step(4)
        self.assertFalse(done)
        self.assertEqual(len(observation), 82)
        self.assertNotEqual(reward, 0.0)
        _ = self.env.reset()
        # just don't crash when we call `render()`
        f = self.env.render(mode='return_figure')
        self.env.close()

    def test_multi_step(self):
        # observation is 20 x 4 sensor readings, setting, time
        observation, reward, done, d = self.env.step(4)
        self.assertAlmostEqual(observation[-2], 10.0)
        self.assertAlmostEqual(observation[-1], 0.01)
        observation, reward, done, d = self.env.step(4)
        self.assertAlmostEqual(observation[-2], 10.0)
        self.assertAlmostEqual(observation[-1], 0.02)
        observation, reward, done, d = self.env.step(4)
        self.assertAlmostEqual(observation[-2], 10.0)
        self.assertAlmostEqual(observation[-1], 0.03)
        self.assertFalse(done)
        self.assertTrue(reward < 0.0)
        observation = self.env.reset()
        self.assertAlmostEqual(observation[-2], 10.0)
        self.assertAlmostEqual(observation[-1], 0.00)
        observation, reward, done, d = self.env.step(4)
        self.assertAlmostEqual(observation[-2], 10.0)
        self.assertAlmostEqual(observation[-1], 0.01)
        self.assertTrue(reward < 0.0)

    def test_actions(self):
        observation, reward, done, d = self.env.step(4)
        self.assertAlmostEqual(observation[-2], 10.0)
        self.assertAlmostEqual(observation[-1], 0.01)
        self.assertTrue(reward < 0.0)

        observation = self.env.reset()
        self.assertAlmostEqual(observation[-1], 0.00)
        observation, reward, done, d = self.env.step(0)
        self.assertAlmostEqual(observation[-2], 9.5)
        self.assertAlmostEqual(observation[-1], 0.01)
        self.assertTrue(reward < 0.0)

        observation = self.env.reset()
        self.assertAlmostEqual(observation[-1], 0.00)
        observation, reward, done, d = self.env.step(8)
        self.assertAlmostEqual(observation[-2], 10.5)
        self.assertAlmostEqual(observation[-1], 0.01)
        self.assertFalse(done)
        self.assertTrue(reward < 0.0)

        # print(observation)
