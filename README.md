# various_minesweeper

평범한 지뢰찾기 게임에 변화를 주었습니다.  

행 개수, 열 개수를 통한 게임판 사이즈가 변경 가능하며
난이도, 모드 또한 설정 가능합니다.

**난이도**   

난이도는 쉬움, 중간, 어려움이 있으며
난이도가 올라갈수록 지뢰의 개수가 증가합니다.

**모드**  

일반 모드 : 평범한 지뢰찾기 게임과 동일합니다. 게임판의 숫자는 상하좌우 대각선으로 인접한 지뢰의 수를 나타냅니다.
![normal](images/normal.png)

십자 모드 : 게임판의 숫자는 가로세로 2칸의 십자 모양으로 인접한 지뢰의 수를 나타냅니다.
![cross](images/cross.png)

나이트 모드 : 게임판의 숫자는 체스의 나이트의 움직임 모양으로 인접한 지뢰의 수를 나타냅니다.
![knight](images/knight.png)

이 프로젝트는 ripexz님의 [python-tkinter-minesweeper](https://github.com/ripexz/python-tkinter-minesweeper) 프로젝트를 이용했습니다.  

해당 코드에서 작동하지 않는 문제와 행 개수, 열 개수, 난이도, 모드를 설정하는 부분을 추가했습니다.
