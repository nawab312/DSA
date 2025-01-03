class Solution(object):
    def reverseVowels(self, s):
        vowels = "aieouAIEOU"
        s = list(s)
        left = 0
        right = len(s) - 1

        while right >= left:
            if s[left] not in vowels:
                left += 1
            elif s[right] not in vowels:
                right -= 1
            else:
                s[left], s[right] = s[right], s[left]
                left += 1
                right -= 1
        s = ''.join(s)
        return s
            
        
