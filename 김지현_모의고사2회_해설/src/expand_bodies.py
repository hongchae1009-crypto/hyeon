"""2회 전공 문항(교육론 제외)의 풀이 본문을 단계별 상세 풀이로 바꾼다.

각 문항에서 '2027 출제 가능성' 상자 뒤부터 '**채점 포인트·함정**' 앞까지를 아래 본문으로 교체한다.
한 번만 실행한다(이미 바뀐 문항은 '**주어진 것 / 구할 것**'이 있어 건너뛴다).
"""
import os, re

MD = os.path.join(os.path.dirname(__file__), '..', '김지현_모의고사2회_상세해설.md')

def mech(name, title):
    return f'**메커니즘 — {title}**\n\n<img class="s mech" src="img/{name}.svg" alt="{title}">\n\n'

B = {}

B['a1'] = r"""
**주어진 것 / 구할 것**

- 반응 $2A \rightleftharpoons A_2$, 정반응 속도상수 $k_a$(속도 $= k_a[A]^2$), 역반응 $k_a'$(속도 $= k_a'[A_2]$)
- $[A]_{tot} = [A]_{eq} + 2[A_2]_{eq}$
- 구할 것: 완화 시간 $\tau$, 그리고 $1/\tau^2$을 $[A]_{tot}, k_a, k_a'$로

**풀이 전략** 평형에서 아주 조금 벗어난 양 $x$를 두고 속도식을 $x$에 대해 1차까지만 전개(선형화)하면 $dx/dt = -x/\tau$ 꼴이 됩니다. 그 계수가 $1/\tau$입니다.

**단계별 풀이**

1. A의 알짜 변화 속도(A는 2개씩 소모·생성):

$$\frac{d[A]}{dt} = -2k_a[A]^2 + 2k_a'[A_2]$$

2. 평형 조건(알짜 속도 0):

$$k_a[A]_{eq}^2 = k_a'[A_2]_{eq}$$

3. 변위 정의: $[A] = [A]_{eq} + x$. A가 $x$만큼 늘면 $A_2$는 $x/2$만큼 줄어야 하므로 $[A_2] = [A_2]_{eq} - \tfrac{x}{2}$.

4. 대입하고 전개:

$$\begin{aligned}
\frac{dx}{dt} &= -2k_a\left([A]_{eq}^2 + 2[A]_{eq}x + x^2\right) + 2k_a'\left([A_2]_{eq} - \tfrac{x}{2}\right)\\
&= \underbrace{\left(-2k_a[A]_{eq}^2 + 2k_a'[A_2]_{eq}\right)}_{=0\ (\text{단계 2})} - 4k_a[A]_{eq}x - k_a'x - 2k_ax^2
\end{aligned}$$

5. $x$가 작으므로 $x^2$ 항을 버리면

$$\frac{dx}{dt} = -\left(4k_a[A]_{eq} + k_a'\right)x \;\Rightarrow\; x = x_0e^{-t/\tau},\quad \frac{1}{\tau} = 4k_a[A]_{eq} + k_a'$$

6. 측정 가능한 $[A]_{tot}$로 바꾸기 위해 제곱:

$$\frac{1}{\tau^2} = 16k_a^2[A]_{eq}^2 + 8k_ak_a'[A]_{eq} + k_a'^2$$

7. 첫 항에 평형 조건(단계 2)을 넣으면

$$16k_a^2[A]_{eq}^2 = 16k_a\left(k_a[A]_{eq}^2\right) = 16k_ak_a'[A_2]_{eq} = 8k_ak_a'\left(2[A_2]_{eq}\right)$$

8. 따라서

$$\frac{1}{\tau^2} = 8k_ak_a'\left([A]_{eq} + 2[A_2]_{eq}\right) + k_a'^2 = 8k_ak_a'[A]_{tot} + (k_a')^2$$

**검산** $[A]_{tot} \to 0$이면 $1/\tau \to k_a'$(이합체가 거의 없어 역반응만 남음)로 물리적으로 맞습니다. $1/\tau^2$ 대 $[A]_{tot}$ 그래프는 기울기 $8k_ak_a'$, 절편 $k_a'^2$인 직선 → 두 속도상수를 모두 구할 수 있습니다.

"""

B['a2'] = r"""
**주어진 것 / 구할 것**

- EDTA 0.100 M × 50.0 mL, Hg(ClO₄)₂ 0.100 M × 10.0 mL, pH 10.0
- $\alpha_{Y^{4-}} = 0.25$, $K_f(\mathrm{HgY^{2-}}) = 10^{22.0}$, $E^\circ(\mathrm{Hg^{2+}/Hg}) = 0.852$ V, $\frac{2.303RT}{F} = 0.0600$ V
- 기준 전극 = 표준 수소 전극(0 V). 구할 것: 전지 전압

**풀이 전략** EDTA가 과량이므로 Hg²⁺는 거의 다 착물이 됩니다. 남은 아주 작은 [Hg²⁺]를 **조건 형성상수**로 구해 Hg 전극의 네른스트 식에 넣습니다.

**단계별 풀이**

1. 몰수:

$$n_{\mathrm{EDTA}} = 0.100 \times 50.0 = 5.00\ \mathrm{mmol},\quad n_{\mathrm{Hg}} = 0.100 \times 10.0 = 1.00\ \mathrm{mmol}$$

2. 1 : 1 반응 $\mathrm{Hg^{2+} + EDTA \rightarrow HgY^{2-}}$ 후: HgY²⁻ 1.00 mmol, 남은 EDTA 4.00 mmol, 전체 부피 60.0 mL

$$[\mathrm{HgY^{2-}}] = \frac{1.00}{60.0} = 0.01667\ \mathrm{M},\quad [\mathrm{EDTA}]_{\text{남음}} = \frac{4.00}{60.0} = 0.06667\ \mathrm{M}$$

3. 조건 형성상수(pH 10에서 EDTA 중 Y⁴⁻ 형태는 25 %):

$$K_f' = \alpha_{Y^{4-}}K_f = 0.25 \times 10^{22.0} = 2.5\times10^{21}$$

4. $K_f' = \dfrac{[\mathrm{HgY^{2-}}]}{[\mathrm{Hg^{2+}}][\mathrm{EDTA}]}$를 [Hg²⁺]에 대해 풀기:

$$[\mathrm{Hg^{2+}}] = \frac{0.01667}{(2.5\times10^{21})(0.06667)} = \frac{1}{2.5\times10^{21}\times4} = 1.0\times10^{-22}\ \mathrm{M}$$

5. Hg 전극(지시 전극) 전위, $\mathrm{Hg^{2+} + 2e^- \rightarrow Hg(l)}$, $n = 2$:

$$E_{\mathrm{Hg}} = 0.852 - \frac{0.0600}{2}\log\frac{1}{[\mathrm{Hg^{2+}}]} = 0.852 - 0.0300 \times 22.0 = 0.852 - 0.660 = 0.192\ \mathrm{V}$$

6. 전지 전압 $= E_{\text{지시}} - E_{\text{기준}} = 0.192 - 0 = 0.192$ V

**검산** 부피가 [HgY]/[EDTA] 비에서 약분되므로 몰수비 1 : 4만으로도 $[\mathrm{Hg^{2+}}] = 1/(4K_f')$가 됩니다. Hg²⁺가 $10^{-22}$ M까지 줄어 전위가 표준값보다 0.660 V 낮아진 것도 착물 형성이 매우 강하다는 것과 맞습니다.

"""

B['a3'] = r"""
**주어진 것 / 구할 것**

- MS: M⁺ 365/367/369 (1 : 2 : 1), 286/288 (1 : 1)
- IR: 1750, 1515, 1345 cm⁻¹, 3000 cm⁻¹ 위 O–H/N–H 없음
- ¹³C(DEPT 포함), ¹H NMR 스펙트럼. 구할 것: 구조

**풀이 전략** MS로 할로젠 수 → IR로 작용기 → ¹H 적분·갈라짐으로 조각 → ¹³C/DEPT로 탄소 수 확인 → 분자식·불포화도로 조립하는 순서로 갑니다.

**단계별 풀이**

1. **MS 동위원소 패턴.** ⁷⁹Br : ⁸¹Br ≈ 1 : 1이므로 Br 1개 → M : M+2 = 1 : 1, Br 2개 → $(1+1)^2$ 전개로 1 : 2 : 1. 따라서 **Br 2개**. 365 − 286 = 79 → Br 하나가 떨어진 조각(남은 Br 1개라 286/288 = 1 : 1).
2. **IR.** 1750 cm⁻¹(강): 콘쥬게이션되지 않은 에스터 C=O. 1515/1345 cm⁻¹: NO₂의 비대칭·대칭 신축(방향족 니트로기). O–H, N–H 띠 없음.
3. **¹H NMR 조각** (적분비 2 : 2 : 1 : 1 : 3)

| δ (ppm) | 적분 | 갈라짐 | 배정 | 근거 |
|---|---|---|---|---|
| 8.25 | 2H | d | NO₂ 옆 방향족 H | NO₂가 강한 전자 끌개 → 가장 낮은 장 |
| 7.6 | 2H | d | 반대쪽 방향족 H | AA′BB′ = *para* 이치환 |
| 5.4 | 1H | d | Ar–C**H**Br– | 벤질 + Br, 이웃 H 1개 |
| 4.8 | 1H | d | –C**H**Br–CO₂ | Br + C=O, 이웃 H 1개 |
| 3.9 | 3H | s | OCH₃ | 에스터 메톡시 |

두 CH 이중선은 서로만 짝지음(같은 J) → **–CHBr–CHBr–** 단위.

4. **¹³C/DEPT.** ~168(C=O, DEPT에서 사라짐), ~148·~144(C–NO₂, 고리 ipso, 사라짐), 129·124(방향족 CH ↑), 53(OCH₃ ↑), ~50·~46(CHBr 두 개 ↑) → 고리 대칭으로 신호 8개 = 탄소 10개.
5. **조립.** O₂N–C₆H₄–CHBr–CHBr–CO₂CH₃ = C₁₀H₉Br₂NO₄

$$M(^{79}\mathrm{Br}_2) = 10(12) + 9(1) + 2(79) + 14 + 4(16) = 365\ ✓$$

6. **불포화도.**

$$\mathrm{DBE} = \frac{2C + 2 + N - H - X}{2} = \frac{20 + 2 + 1 - 9 - 2}{2} = 6$$

벤젠 고리 4 + C=O 1 + N=O 1 = 6 ✓

**검산** 이 화합물은 methyl 4-nitrocinnamate에 Br₂가 첨가된 생성물로, 두 CHBr의 화학적 이동(벤질 쪽이 더 낮은 장)과 1 : 2 : 1 패턴이 모두 맞습니다.

"""

B['a4'] = r"""
**주어진 것 / 구할 것**

- MoH₆, 정팔면체($O_h$), H 6개가 ±x, ±y, ±z 축 위
- $O_h$ 지표표. 구할 것: 6개 σ 결합의 가약 표현 → 기약표현의 합, 각 SALC 그림

**풀이 전략** 각 Mo–H σ 벡터를 기저로 삼아, 대칭 조작마다 **제자리에 남는 벡터 수**를 세어 $\Gamma_\sigma$를 만들고 축소 공식으로 분해합니다.

**단계별 풀이**

1. **제자리 벡터 수 세기** (번호: σ₁ +x, σ₂ +y, σ₃ −x, σ₄ −y, σ₅ +z, σ₆ −z)

| 조작 | 남는 벡터 | χ |
|---|---|---|
| E | 6개 모두 | 6 |
| C₃ (몸체 대각선) | 없음(세 축을 돌림) | 0 |
| C₂ (모서리 중점 축) | 없음 | 0 |
| C₄ (z축) | σ₅, σ₆ | 2 |
| C₂ (= C₄², z축) | σ₅, σ₆ | 2 |
| i | 없음(+x ↔ −x) | 0 |
| S₄ | 없음 | 0 |
| S₆ | 없음 | 0 |
| σh (xy면) | σ₁~σ₄ | 4 |
| σd (z축 포함 대각면) | σ₅, σ₆ | 2 |

$$\Gamma_\sigma = (6,\ 0,\ 0,\ 2,\ 2,\ 0,\ 0,\ 0,\ 4,\ 2)$$

2. **축소 공식** $n_i = \frac{1}{h}\sum_R g_R\,\chi_i(R)\,\chi_\sigma(R)$, $h = 48$. 0이 아닌 열(E, 6C₄, 3C₂, 3σh, 6σd)만 계산:

$$\begin{aligned}
n(A_{1g}) &= \tfrac{1}{48}\left[1(1)(6) + 6(1)(2) + 3(1)(2) + 3(1)(4) + 6(1)(2)\right] = \tfrac{48}{48} = 1\\
n(A_{2g}) &= \tfrac{1}{48}\left[6 - 12 + 6 + 12 - 12\right] = 0\\
n(E_g) &= \tfrac{1}{48}\left[2(6) + 6(0)(2) + 3(2)(2) + 3(2)(4) + 6(0)(2)\right] = \tfrac{12 + 12 + 24}{48} = 1\\
n(T_{1g}) &= \tfrac{1}{48}\left[18 + 12 - 6 - 12 - 12\right] = 0\\
n(T_{2g}) &= \tfrac{1}{48}\left[18 - 12 - 6 - 12 + 12\right] = 0\\
n(A_{1u}) &= \tfrac{1}{48}\left[6 + 12 + 6 - 12 - 12\right] = 0\\
n(A_{2u}) &= \tfrac{1}{48}\left[6 - 12 + 6 - 12 + 12\right] = 0\\
n(E_u) &= \tfrac{1}{48}\left[12 + 0 + 12 - 24 + 0\right] = 0\\
n(T_{1u}) &= \tfrac{1}{48}\left[18 + 12 - 6 + 12 + 12\right] = \tfrac{48}{48} = 1\\
n(T_{2u}) &= \tfrac{1}{48}\left[18 - 12 - 6 + 12 - 12\right] = 0
\end{aligned}$$

$$\Gamma_\sigma = A_{1g} + E_g + T_{1u}\quad(1 + 2 + 3 = 6\ ✓)$$

3. **각 SALC와 짝이 되는 Mo 오비탈** (같은 기약표현끼리만 겹침)

| 기약표현 | Mo 오비탈 | SALC (정규화) |
|---|---|---|
| $A_{1g}$ | 5s | $\frac{1}{\sqrt6}(\sigma_1+\sigma_2+\sigma_3+\sigma_4+\sigma_5+\sigma_6)$ |
| $E_g$ | $4d_{z^2}$ | $\frac{1}{\sqrt{12}}(2\sigma_5+2\sigma_6-\sigma_1-\sigma_2-\sigma_3-\sigma_4)$ |
| $E_g$ | $4d_{x^2-y^2}$ | $\frac12(\sigma_1-\sigma_2+\sigma_3-\sigma_4)$ |
| $T_{1u}$ | $5p_x, 5p_y, 5p_z$ | $\frac{1}{\sqrt2}(\sigma_1-\sigma_3)$, $\frac{1}{\sqrt2}(\sigma_2-\sigma_4)$, $\frac{1}{\sqrt2}(\sigma_5-\sigma_6)$ |

4. **그림 그리는 규칙.** 중심 오비탈 로브의 부호와 **같은 부호**로 H 1s를 칠합니다. $A_{1g}$: 6개 모두 같은 색. $d_{z^2}$: z축 두 개 큰 +, xy면 네 개 작은 −. $d_{x^2-y^2}$: x축 둘 +, y축 둘 −. $p_x$: +x는 +, −x는 −, 나머지 넷은 0.

**검산** $t_{2g}$($d_{xy}, d_{xz}, d_{yz}$)는 축 사이를 향하므로 σ SALC가 없고(축소 결과 $T_{2g}$ = 0) 비결합으로 남습니다.

"""

B['a8'] = r"""
**주어진 것 / 구할 것**

- $\psi_n = \sqrt{\tfrac{2}{L}}\sin\tfrac{n\pi x}{L}$ ($0 \le x \le L$), 적분 공식 3개
- 구할 것: $\langle x\rangle, \langle x^2\rangle, \langle p\rangle, \langle p^2\rangle$, $\Delta x\Delta p$ ($\pi$, $n$ 포함)

**풀이 전략** 기대치 $\langle A\rangle = \int\psi^*\hat A\psi\,dx$를 적분 공식으로 계산하고, $\Delta A = \sqrt{\langle A^2\rangle - \langle A\rangle^2}$를 씁니다. $b = n\pi/L$로 두면 경계에서 $\sin(2bL) = \sin 2n\pi = 0$, $\cos(2bL) = 1$입니다.

**단계별 풀이**

1. **⟨x⟩** (두 번째 공식)

$$\langle x\rangle = \frac2L\left[\frac{x^2}{4} - \frac{x}{4b}\sin 2bx - \frac{\cos 2bx}{8b^2}\right]_0^L = \frac2L\left[\frac{L^2}{4} - 0 - \frac{1}{8b^2} + \frac{1}{8b^2}\right] = \frac{L}{2}$$

2. **⟨x²⟩** (세 번째 공식)

$$\begin{aligned}
\langle x^2\rangle &= \frac2L\left[\frac{x^3}{6} - \left(\frac{x^2}{4b} - \frac{1}{8b^3}\right)\sin 2bx - \frac{x}{4b^2}\cos 2bx\right]_0^L\\
&= \frac2L\left[\frac{L^3}{6} - 0 - \frac{L}{4b^2}\right] = \frac{L^2}{3} - \frac{1}{2b^2}\\
&= L^2\left(\frac13 - \frac{1}{2n^2\pi^2}\right)
\end{aligned}$$

3. **Δx**

$$\Delta x = \sqrt{\langle x^2\rangle - \langle x\rangle^2} = L\sqrt{\frac13 - \frac14 - \frac{1}{2n^2\pi^2}} = L\sqrt{\frac{1}{12} - \frac{1}{2n^2\pi^2}}$$

4. **⟨p⟩**, $\hat p = -i\hbar\frac{d}{dx}$:

$$\langle p\rangle = -i\hbar\frac2L\cdot b\int_0^L\sin bx\cos bx\,dx = -i\hbar\frac{b}{L}\int_0^L\sin 2bx\,dx = -i\hbar\frac{b}{L}\left[-\frac{\cos 2bx}{2b}\right]_0^L = 0$$

5. **⟨p²⟩**, $\frac{d^2}{dx^2}\sin bx = -b^2\sin bx$이므로 $\hat p^2\psi = \hbar^2b^2\psi$:

$$\langle p^2\rangle = \hbar^2b^2\underbrace{\int_0^L\psi^2dx}_{=1} = \frac{n^2\pi^2\hbar^2}{L^2} = \frac{n^2h^2}{4L^2}$$

(검산: $\langle p^2\rangle/2m = n^2h^2/8mL^2 = E_n$ ✓)

6. **Δp**: $\Delta p = \sqrt{\langle p^2\rangle - 0} = \dfrac{n\pi\hbar}{L} = \dfrac{nh}{2L}$

7. **곱**

$$\Delta x\Delta p = n\pi\hbar\sqrt{\frac{1}{12} - \frac{1}{2n^2\pi^2}} = \frac{\hbar}{2}\sqrt{\frac{n^2\pi^2}{3} - 2} = \frac{nh}{2}\sqrt{\frac{1}{12} - \frac{1}{2n^2\pi^2}}$$

**검산** n = 1: $\frac{\hbar}{2}\sqrt{3.290 - 2} = 0.568\hbar > 0.5\hbar$, n = 2: $1.67\hbar$. 모든 n에서 불확정성 원리를 만족하고 n이 클수록 커집니다.

"""

B['a9'] = r"""
**주어진 것 / 구할 것**

| L | $K_d$ | $\nu_{CO}$ (cm⁻¹) | 원뿔각 |
|---|---|---|---|
| PEt₃ | 1 | 1985 | 132° |
| PPr₃ | 1.1 | 1980 | 135° |
| PEt₂Ph | 2.5 | 1990 | 135° |
| PEtPh₂ | 24 | 1990 | 140° |
| PPh₃ | 750 | 1995 | 145° |

구할 것: νCO와 Co–CO 결합 세기의 관계, PEt₃ vs PPr₃의 $K_d$ 해석, PPh₃의 $K_d$가 큰 이유

**풀이 전략** $K_d$에 영향을 주는 두 인자를 나눠 봅니다. ① **전자 효과**(νCO로 읽음: 역결합 정도), ② **입체 효과**(원뿔각). 한 인자가 같은 쌍을 비교하면 다른 인자의 효과만 분리됩니다.

**단계별 풀이**

1. **νCO와 결합 세기.** Co의 d 전자가 CO π*로 들어가는 역결합이 클수록 Co–C 결합 차수↑, C≡O 결합 차수↓ → νCO↓. 반대로 **νCO가 클수록 역결합이 적어 Co–CO 결합이 약하고** CO가 잘 떨어집니다.
2. **해리 자유 에너지로 환산** ($\Delta G^\circ = -RT\ln K_d$, 298 K): PEt₃ 0, PPr₃ −0.24, PEt₂Ph −2.3, PEtPh₂ −7.9, PPh₃ −16.4 kJ/mol. PPh₃는 PEt₃보다 해리가 16 kJ/mol 유리합니다.
3. **입체 효과만 비교** (원뿔각이 같은 PPr₃ vs PEt₂Ph, 둘 다 135°): νCO 1980 → 1990으로 커질 때 $K_d$ 1.1 → 2.5. 전자 효과 자체는 존재하지만 작습니다(2배 정도).
4. **PEt₃ vs PPr₃.** νCO만 보면 PEt₃(1985)가 역결합이 더 약해 CO가 더 잘 떨어져야 합니다. 그런데 실제로는 PPr₃의 $K_d$가 약간 더 큽니다(1.1 > 1). 원뿔각이 132° → 135°로 커져 **입체 반발이 해리를 돕는 효과가 전자 효과를 넘어섰기** 때문입니다. 다만 차이가 작은 것은 두 효과가 서로 상쇄되기 때문입니다.
5. **PPh₃.** 원뿔각 145°로 가장 큽니다. 포스핀 두 개와 Br 두 개, CO가 금속 주위를 차지하면 리간드끼리 반발이 커서, CO가 떨어져 4배위 CoBr₂L₂가 되면 반발이 크게 풀립니다. νCO(1995)도 가장 커서 역결합도 가장 약하므로 **두 효과가 같은 방향** → $K_d$ = 750.

**검산** 원뿔각 132 → 145°(13° 증가)에 $K_d$가 750배, νCO 1980 → 1990(같은 원뿔각)에서는 2배 → 이 계열에서는 입체 효과가 지배적입니다.

"""

B['a10'] = r"""
**주어진 것 / 구할 것**

- 출발물 1,2-dibromopropane, 시약 순서: (1) NaNH₂ 3당량 (2) HA → H₂ 1당량, Ni₂B(P-2) → A → Cl₂ 400 °C → Cl₂/H₂O → B → HO⁻ 1당량 → C → HO⁻ 과량 → D
- D의 ¹H NMR(D₂O). 구할 것: A~D, 3.75 ppm 피크의 수소

**풀이 전략** 각 시약이 하는 일을 한 줄로 정리한 뒤, 탄소 3개 골격을 끝까지 따라갑니다. 위치 선택성은 중간체(라디칼, 클로로늄 이온)의 안정성으로 판단합니다.

**단계별 풀이**

1. **NaNH₂ 3당량** — 비자리(vicinal) 이브로민화물의 E2 두 번 → propyne. 세 번째 NH₂⁻는 말단 ≡C–H(pKa ≈ 25)를 떼어 아세틸라이드를 만들어 평형을 생성물 쪽으로 끌고, (2) HA(약산) 처리에서 다시 양성자화됩니다.
2. **H₂ 1당량, Ni₂B(P-2)** — 독이 든 촉매라 알카인 → 알켄에서 멈춤(syn 첨가) → **A propene** CH₂=CH–CH₃.
3. **Cl₂, 400 °C** — 고온에서는 Cl₂ 첨가가 가역적이고, Cl·가 **알릴 H**(C–H 결합 해리 에너지 ≈ 369 kJ/mol로 가장 약함)를 떼어 공명 안정화된 알릴 라디칼을 만듭니다 → allyl chloride ClCH₂–CH=CH₂.
4. **Cl₂/H₂O** — C=C가 Cl₂를 공격해 **클로로늄 이온**. 물은 양전하를 더 잘 나눠 갖는 **더 치환된 탄소(C2)**를 뒷면에서 공격(Markovnikov) → 탈양성자화 → **B** ClCH₂–CH(OH)–CH₂Cl (1,3-dichloro-2-propanol).
5. **HO⁻ 1당량** — 산성이 가장 큰 OH를 떼어 알콕사이드 → 이웃 C–Cl 탄소를 분자 내 S<sub>N</sub>2 공격(3원 고리, 빠름) → **C** epichlorohydrin.
6. **HO⁻ 과량** — 남은 CH₂Cl의 S<sub>N</sub>2 치환, 에폭사이드는 염기 조건이라 **덜 치환된 CH₂**에서 개환 → 양성자화 → **D glycerol** HOCH₂–CH(OH)–CH₂OH.

**D의 ¹H NMR 배정** (D₂O에서 OH는 D로 교환되어 HOD 신호 4.8~5.3 ppm에 합쳐짐)

| δ (ppm) | 적분 | 배정 | 근거 |
|---|---|---|---|
| 3.75 | 1H | 가운데 **CH**(OH) | 이웃 CH₂ 두 개(4H)와 짝지음 → 다중선, 1H |
| 3.55~3.65 | 4H | 양 끝 CH₂ | 대칭으로 같은 환경, 부분입체 수소라 복잡한 dd |

**왜 이 생성물인가** 400 °C에서는 엔트로피 때문에 첨가 생성물이 불리하고 라디칼 연쇄가 우세합니다. 반면 Cl₂/H₂O(실온, 극성 용매)에서는 이온성 첨가가 일어나 H₂O가 할로늄의 더 치환된 탄소를 공격합니다. 같은 Cl₂라도 조건이 생성물을 바꿉니다.

""" + mech('m_A10_e2', '이중 E2와 아세틸라이드 (→ A)') + mech('m_A10_radical', '알릴 라디칼 염소화') + mech('m_A10_halohydrin', '클로로하이드린 형성 (→ B)') + mech('m_A10_epox', '에폭사이드 형성과 개환 (→ C, D)') + r"""**검산** 분자식: A C₃H₆ → allyl chloride C₃H₅Cl → B C₃H₆Cl₂O → C C₃H₅ClO → D C₃H₈O₃. 탄소 3개가 끝까지 유지됩니다.

"""

B['a11'] = r"""
**주어진 것 / 구할 것**

- 벤즈알데하이드(α-H 없음) 2분자 + HO⁻ → A + B
- 벤즈알데하이드 + 니트로에테인, 묽은 HO⁻ → C + H₂O
- 벤즈알데하이드 + 알릴리덴 일라이드 (C₆H₅)₃P⁺–C⁻H–CH=CH₂ → D
- 구할 것: A, B 구조와 메커니즘, C·D 구조

**풀이 전략** α-H가 없는 알데하이드는 엔올레이트를 만들 수 없어, 진한 염기에서 **Cannizzaro(불균등화)**를 합니다. 니트로에테인은 α-H가 매우 산성(pKa ≈ 8.6)이라 엔올레이트 대신 **니트로네이트**가 친핵체가 됩니다(Henry). 일라이드는 C=O를 C=C로 바꿉니다(Wittig).

**단계별 풀이 — A, B (Cannizzaro)**

1. HO⁻가 PhCHO의 C=O 탄소를 공격 → 사면체 알콕사이드 PhCH(OH)O⁻.
2. (진한 염기에서는) O–H가 한 번 더 탈양성자화되어 이음이온 PhCH(O⁻)₂ — 전자가 더 풍부해 H⁻를 더 잘 내놓습니다(속도 ∝ [PhCHO]²[HO⁻]² 항).
3. 사면체 중간체에서 C=O가 다시 생기며 **H⁻가 두 번째 PhCHO의 카보닐 탄소로 직접 이동**(이 단계가 속도 결정 단계).
4. 결과: PhCOOH + PhCH₂O⁻ → 바로 산–염기 반응 → **PhCOO⁻ + PhCH₂OH**. 산 처리하면 **A 벤조산**, **B 벤질 알코올**.
5. 산화수로 확인: 카보닐 C +1 → 카복실 C +3(산화), CH₂OH의 C −1(환원) → 불균등화.

**단계별 풀이 — C (Henry 반응 + 탈수)**

1. HO⁻가 CH₃CH₂NO₂의 α-H 제거 → 니트로네이트(음전하가 O로 비편재화).
2. 니트로네이트의 탄소가 PhCHO의 C=O 공격 → 알콕사이드 → 양성자화 → β-니트로알코올 PhCH(OH)CH(CH₃)NO₂.
3. NO₂ 옆 α-H가 산성이라 다시 떼어지고, OH⁻가 이탈하는 **E1cB 탈수** → 콘쥬게이션된 니트로알켄 **C** PhCH=C(CH₃)NO₂. 부피 큰 Ph와 NO₂가 반대쪽인 (E)가 주생성물.

**단계별 풀이 — D (Wittig)**

1. 일라이드 탄소(C⁻)가 C=O 탄소를 공격, O⁻가 P⁺로 → 4원 고리 **옥사포스페테인**.
2. 고리가 깨지며 매우 강한 P=O(≈ 575 kJ/mol)가 생기는 것이 구동력 → Ph₃P=O + **D** PhCH=CH–CH=CH₂ (1-phenyl-1,3-butadiene).

""" + mech('m_A11_cannizzaro', 'Cannizzaro 반응 (→ A, B)') + mech('m_A11_henry', 'Henry 반응과 탈수 (→ C)') + mech('m_A11_wittig', 'Wittig 반응 (→ D)') + r"""**왜 이 생성물인가** 벤즈알데하이드는 α-H가 없어 aldol을 할 수 없으므로 염기와는 Cannizzaro만 가능합니다. 니트로에테인이 함께 있으면 니트로네이트가 훨씬 쉽게 생겨(pKa 8.6 ≪ 알데하이드 α-H) 교차 축합(Henry)이 우선합니다. 탈수 생성물은 벤젠 고리–C=C–NO₂로 이어진 긴 콘쥬게이션 덕분에 안정합니다.

**검산** C: C₇H₆O + C₂H₅NO₂ − H₂O = C₉H₉NO₂ ✓, D: C₇H₆O + C₃H₄(일라이드 부분) − O = C₁₀H₁₀ ✓

"""

B['a12'] = r"""
**주어진 것 / 구할 것**

- MES 0.02000 M × 50.00 mL, NaOH 0.1000 M, pKa 6.300, 당량점 pH 9.250
- 티몰프탈레인 종말점 pH 10.00. 구할 것: 최대 기울기 부피, 완충력 최대 지점, pH 10.00까지 넣은 부피

**풀이 전략** 당량점(기울기 최대), 반당량점(기울기 최소 = 완충 용량 최대)을 구하고, 당량점 이후는 **과량 OH⁻**로 pH가 정해진다는 것을 이용합니다.

**단계별 풀이**

1. **당량점**: $n_{\mathrm{MES}} = 0.02000 \times 50.00 = 1.000$ mmol

$$V_e = \frac{1.000\ \mathrm{mmol}}{0.1000\ \mathrm{M}} = 10.00\ \mathrm{mL}\quad(\text{기울기 최대})$$

2. **반당량점** $V_b = 5.00$ mL에서 [HA] = [A⁻] → $\mathrm{pH} = \mathrm{p}K_a + \log 1 = 6.300$. 완충 용량

$$\beta = 2.303\,C\frac{K_a[\mathrm{H^+}]}{(K_a + [\mathrm{H^+}])^2}$$

은 $[\mathrm{H^+}] = K_a$일 때 최대 → pH 변화에 대한 저항력이 가장 큰 지점(곡선 기울기 최소).

3. **당량점 pH 확인**: $[\mathrm{A^-}] = 1.000/60.00 = 0.01667$ M, $K_b = 10^{-14}/10^{-6.3} = 2.0\times10^{-8}$

$$[\mathrm{OH^-}] = \sqrt{K_bC} = \sqrt{2.0\times10^{-8}\times0.01667} = 1.82\times10^{-5} \Rightarrow \mathrm{pH} = 9.26\ ✓$$

4. **pH 10.00까지**: 당량점을 지나 넣은 NaOH를 $\delta$ mL라 하면 과량 OH⁻가 pH를 결정

$$[\mathrm{OH^-}] = 10^{-4.00} = \frac{0.1000\,\delta}{50.00 + 10.00 + \delta}$$

$$1.00\times10^{-4}(60.00 + \delta) = 0.1000\,\delta \;\Rightarrow\; \delta = \frac{6.00\times10^{-3}}{0.1000 - 0.0001} = 0.0600\ \mathrm{mL}$$

$$V = 10.00 + 0.06 = 10.06\ \mathrm{mL}$$

5. **엄밀 확인**: pH 10에서 $[\mathrm{HA}] = [\mathrm{A^-}]\dfrac{[\mathrm{H^+}]}{K_a} = 0.01665 \times 10^{-3.7} = 3.3\times10^{-6}$ M → A⁻ 가수분해가 내는 OH⁻는 $10^{-4}$의 3 %라 결과는 10.058 ≈ **10.06 mL**로 같습니다.

**검산** 적정 오차 = +0.06 mL(+0.6 %). 티몰프탈레인 변색 범위(9.4~10.6)가 당량점 pH(9.25)보다 높아 조금 늦게 끝납니다.

"""

B['b1'] = r"""
**주어진 것 / 구할 것**

- B fumaric acid(trans), E maleic acid(cis)
- (1) OsO₄, pyr (2) NaHSO₃/H₂O → syn 이하이드록시화 / Br₂ → anti 첨가
- 구할 것: A, C, D, F 중 meso와 라셈, 구조

**풀이 전략** 대칭 알켄(양쪽 치환기가 같은 HO₂C–CH=CH–CO₂H)에서는 **알켄 기하(cis/trans) × 첨가 방식(syn/anti)**만으로 결과가 정해집니다. 같은 면에서 둘을 넣으면 원래 배치가 그대로 보존된다고 생각하면 쉽습니다.

**단계별 풀이**

1. **시약의 입체화학.** OsO₄는 [3+2] 협동 첨가로 고리형 오스메이트 에스터 → 두 C–O가 같은 면(**syn**). Br₂는 브로모늄 이온 → Br⁻가 반대 면에서 공격(**anti**).
2. **네 가지 조합**

| 출발물 | 시약 | 첨가 | 생성물 | 판정 |
|---|---|---|---|---|
| B (trans) | OsO₄ | syn | **A** 타타르산 | (2R,3R) + (2S,3S) **라셈** |
| B (trans) | Br₂ | anti | **C** 2,3-dibromosuccinic acid | (2R,3S) **meso** |
| E (cis) | OsO₄ | syn | **D** 타타르산 | (2R,3S) **meso** |
| E (cis) | Br₂ | anti | **F** 2,3-dibromosuccinic acid | (2R,3R) + (2S,3S) **라셈** |

3. **R/S 우선순위 정하기 (CIP).**
   - 타타르산 C2: **–OH** (O) > **–COOH** (C에 O,O,O) > **–CH(OH)COOH** (C에 O,C,H) > H
   - 다이브로모숙신산 C2: **–Br** > **–CH(Br)COOH** (C에 Br,C,H — 첫 원자 Br이 O보다 큼) > **–COOH** (C에 O,O,O) > H
4. **meso 판정.** D와 C는 두 입체중심이 (R,S)이고, Fischer 투영식에서 가운데 가로선이 거울면 → 광학 비활성. A와 F는 (R,R)/(S,S)로 거울면이 없고, 대칭 알켄의 양면 공격 확률이 같아 1 : 1 라셈.

""" + mech('m_B01_os', 'OsO₄ syn 이하이드록시화') + mech('m_B01_br', 'Br₂ anti 첨가') + r"""**왜 이 생성물인가** syn 첨가는 알켄의 기하를 그대로 입체배열로 옮기고(cis → 같은 쪽 → meso), anti 첨가는 하나를 뒤집습니다(cis → 반대쪽 → 라셈). 그래서 trans 알켄에서는 결과가 정반대가 됩니다.

**검산** 각 생성물은 입체중심 2개, 이론적 입체이성질체 3개(R,R / S,S / meso) 중 위 표대로 나뉩니다.

"""

B['b2'] = r"""
**주어진 것 / 구할 것**

- 25 °C, I = 0.20 A, R = 5.0 Ω, [Ni²⁺] = 0.010 M, pH 5.0, $P_{O_2}$ = 1.0 atm
- O₂ 발생 과전압 0.50 V, $\mathrm{Ni^{2+} + 2e^- \rightarrow Ni}$ (−0.260 V), $\mathrm{O_2 + 4H^+ + 4e^- \rightarrow 2H_2O}$ (1.24 V)
- 구할 것: Ni 석출에 걸어야 할 초기 전압

**풀이 전략** 전기분해에 필요한 전압 = (평형 전지 전위) − (저항 손실 IR) − (과전압). 먼저 네른스트로 두 전극의 평형 전위를 구합니다.

**단계별 풀이**

1. **환원 전극(Ni)**

$$E_{\mathrm{Ni}} = -0.260 - \frac{0.060}{2}\log\frac{1}{[\mathrm{Ni^{2+}}]} = -0.260 - 0.030\log\frac{1}{0.010} = -0.260 - 0.060 = -0.320\ \mathrm{V}$$

2. **산화 전극(O₂ 발생)**, 환원 반쪽 반응으로 쓰고 $[\mathrm{H^+}] = 10^{-5.0}$

$$E_{\mathrm{O_2}} = 1.24 - \frac{0.060}{4}\log\frac{1}{P_{O_2}[\mathrm{H^+}]^4} = 1.24 - 0.015\log\frac{1}{(1.0)(10^{-5})^4} = 1.24 - 0.015(20) = 0.94\ \mathrm{V}$$

3. **평형 전지 전위** (Ni 쪽이 환원 전극)

$$E_{\text{전지}} = E_{\text{환원}} - E_{\text{산화}} = -0.320 - 0.94 = -1.26\ \mathrm{V}\quad(\text{비자발, 외부 전압 필요})$$

4. **저항 손실**: $IR = 0.20\ \mathrm{A} \times 5.0\ \Omega = 1.0$ V
5. **걸어야 할 전압**

$$E = E_{\text{전지}} - IR - \eta = -1.26 - 1.0 - 0.50 = -2.76\ \mathrm{V}$$

**검산** 전체 반응 $\mathrm{2Ni^{2+} + 2H_2O \rightarrow 2Ni + O_2 + 4H^+}$: $E^\circ = -0.260 - 1.24 = -1.50$ V, $Q = \dfrac{P_{O_2}[\mathrm{H^+}]^4}{[\mathrm{Ni^{2+}}]^2} = \dfrac{10^{-20}}{10^{-4}} = 10^{-16}$, $E = -1.50 - \frac{0.060}{4}\log 10^{-16} = -1.50 + 0.24 = -1.26$ V ✓. "초기" 전압인 이유: Ni²⁺가 줄고 H⁺가 늘면서 필요한 전압이 점점 커지기 때문입니다.

"""

B['b6'] = r"""
**주어진 것 / 구할 것**

- 두 상 공존 조건, Clapeyron 식, $dH = C_pdT + Vdp$
- 정의 $\alpha = \frac1V\left(\frac{\partial V}{\partial T}\right)_p$, $\kappa_T = -\frac1V\left(\frac{\partial V}{\partial p}\right)_T$
- 구할 것: 상 경계를 따른 $d(\Delta H/T)$, 2차 상전이에서 $dp/dT$를 (α, κ)와 ($C_{p,m}$, α)로

**풀이 전략** 1차 상전이는 상 경계를 따라 μ가 같다는 조건에서 Clapeyron 식이 나옵니다. 2차 상전이는 $\Delta V = \Delta S = 0$이라 0/0이 되므로, **V와 S가 경계를 따라 연속(dV₁ = dV₂, dS₁ = dS₂)**이라는 조건을 대신 씁니다(Ehrenfest).

**단계별 풀이 (1) $d(\Delta H/T)$**

1. 각 상에서 $dH_i = C_{p,i}dT + V_idp$ → 빼면 $d\Delta H = \Delta C_pdT + \Delta Vdp$.
2. 상 경계 위에서는 Clapeyron: $\dfrac{dp}{dT} = \dfrac{\Delta H}{T\Delta V}$ → $\Delta V\,dp = \dfrac{\Delta H}{T}dT$.
3. 대입: $d\Delta H = \Delta C_pdT + \dfrac{\Delta H}{T}dT$.
4. 몫의 미분:

$$d\left(\frac{\Delta H}{T}\right) = \frac{d\Delta H}{T} - \frac{\Delta H}{T^2}dT = \frac{\Delta C_p}{T}dT + \frac{\Delta H}{T^2}dT - \frac{\Delta H}{T^2}dT = \Delta C_p\,d\ln T$$

**단계별 풀이 (2) α, κ로 쓴 dp/dT**

1. 부피를 $V(T, p)$로 보고 전미분: $dV = \left(\frac{\partial V}{\partial T}\right)_pdT + \left(\frac{\partial V}{\partial p}\right)_Tdp = V(\alpha\,dT - \kappa_T\,dp)$.
2. 2차 상전이에서는 $V_1 = V_2$이고 경계를 따라서도 같으므로 $dV_1 = dV_2$:

$$V(\alpha_1dT - \kappa_{T,1}dp) = V(\alpha_2dT - \kappa_{T,2}dp)$$

3. 정리:

$$(\kappa_{T,2} - \kappa_{T,1})dp = (\alpha_2 - \alpha_1)dT \;\Rightarrow\; \frac{dp}{dT} = \frac{\alpha_2 - \alpha_1}{\kappa_{T,2} - \kappa_{T,1}}$$

**단계별 풀이 (3) $C_{p,m}$, α로 쓴 dp/dT**

1. 엔트로피 전미분: $dS = \left(\frac{\partial S}{\partial T}\right)_pdT + \left(\frac{\partial S}{\partial p}\right)_Tdp = \dfrac{C_p}{T}dT - \alpha V\,dp$ (맥스웰 관계식 $(\partial S/\partial p)_T = -(\partial V/\partial T)_p$).
2. 1몰 기준 $dS_{m,1} = dS_{m,2}$:

$$\frac{C_{p,m1}}{T}dT - \alpha_1V_mdp = \frac{C_{p,m2}}{T}dT - \alpha_2V_mdp$$

3. 정리:

$$\frac{dp}{dT} = \frac{C_{p,m2} - C_{p,m1}}{TV_m(\alpha_2 - \alpha_1)}$$

**검산** 두 식을 같다고 두면 $\Delta C_{p,m} = TV_m\dfrac{(\Delta\alpha)^2}{\Delta\kappa_T}$ — Ehrenfest 관계식으로 서로 모순 없이 이어집니다.

"""

B['b7'] = r"""
**주어진 것 / 구할 것**

- TMM(가운데 C4에 C1, C2, C3 연결)과 알릴 라디칼의 영년 행렬식
- 구할 것: 각 분자의 전체 π 에너지와 비편재화 에너지

**풀이 전략** 행렬식의 각 행을 β로 나누고 $x = (\alpha - E)/\beta$로 치환해 다항식을 풉니다. 에너지 준위에 전자를 아래부터 채워 합하고, 국소화된 구조(고립된 C=C + 홀전자)와의 차이가 비편재화 에너지입니다.

**단계별 풀이 — TMM**

1. 치환한 행렬식:

$$\begin{vmatrix} x&0&0&1\\0&x&0&1\\0&0&x&1\\1&1&1&x \end{vmatrix} = 0$$

2. 첫 행으로 전개하면 $x\cdot(x^3 - 2x) - 1\cdot(x^2) = x^4 - 3x^2 = x^2(x^2 - 3) = 0$.
3. 해: $x = -\sqrt3, 0, 0, +\sqrt3$ → $E = \alpha - x\beta$:

| x | E | 성격 | 전자 |
|---|---|---|---|
| $-\sqrt3$ | $\alpha + \sqrt3\beta$ | 결합성 | 2 |
| 0 (2개) | $\alpha$ | 비결합(이중 축퇴) | 1 + 1 |
| $+\sqrt3$ | $\alpha - \sqrt3\beta$ | 반결합성 | 0 |

4. π 전자 4개: $E_\pi = 2(\alpha + \sqrt3\beta) + \alpha + \alpha = 4\alpha + 2\sqrt3\beta$. 축퇴된 비결합 MO에 홀전자 2개 → 삼중항 이중 라디칼.
5. 국소화 구조(C=C 하나 + 홀전자 두 개): $2(\alpha + \beta) + 2\alpha = 4\alpha + 2\beta$.
6. 비편재화 에너지: $(4\alpha + 2\sqrt3\beta) - (4\alpha + 2\beta) = (2\sqrt3 - 2)\beta = 1.464\beta$.

**단계별 풀이 — 알릴 라디칼**

1. $\begin{vmatrix} x&1&0\\1&x&1\\0&1&x \end{vmatrix} = x(x^2 - 1) - x = x^3 - 2x = x(x^2 - 2) = 0$ → $x = -\sqrt2, 0, \sqrt2$.
2. MO(정규화 계수):

| E | MO | 전자 |
|---|---|---|
| $\alpha + \sqrt2\beta$ | $\psi_1 = \tfrac12\phi_1 + \tfrac{1}{\sqrt2}\phi_2 + \tfrac12\phi_3$ | 2 |
| $\alpha$ | $\psi_2 = \tfrac{1}{\sqrt2}(\phi_1 - \phi_3)$ (가운데 마디) | 1 |
| $\alpha - \sqrt2\beta$ | $\psi_3 = \tfrac12\phi_1 - \tfrac{1}{\sqrt2}\phi_2 + \tfrac12\phi_3$ | 0 |

3. $E_\pi = 2(\alpha + \sqrt2\beta) + \alpha = 3\alpha + 2\sqrt2\beta$, 국소화 $3\alpha + 2\beta$ → 비편재화 에너지 $(2\sqrt2 - 2)\beta = 0.828\beta$.

**검산** 고윳값의 합 = 행렬의 대각합: TMM $(-\sqrt3) + 0 + 0 + \sqrt3 = 0$ ✓, 알릴 0 ✓. 홀전자가 들어간 알릴 ψ₂는 가운데 탄소에 계수 0 → 라디칼 성질은 양 끝 탄소에만 있습니다(공명 구조 2개와 일치). β < 0이므로 비편재화 에너지는 안정화입니다.

"""

B['b8'] = r"""
**주어진 것 / 구할 것**

- [PdCl₂(NH₃)₂] 이성질체 X, Y(사각 평면). X의 Pd–Cl 신축 IR 띠 2개(320, 280 cm⁻¹)
- 좌표: z 위, y 오른쪽(분자 평면 = yz). C₂ᵥ, C₂ₕ, D₂ₕ, D₂d 지표표
- 구할 것: X의 구조·점군, 두 띠의 기약표현·진동 방식, Y의 IR 활성 기약표현

**풀이 전략** Pd–Cl 결합 두 개를 벡터로 두고, 대칭 조작마다 제자리에 남는 벡터 수로 가약 표현을 만들어 축소합니다. IR 활성은 x, y, z와 같은 기약표현입니다.

**단계별 풀이 — cis 이성질체 (C₂ᵥ)**

1. cis: 두 Cl이 이웃(90°), C₂축은 두 Cl의 이등분선(z). 분자 평면 = σᵥ′(yz).
2. Γ(Pd–Cl): E 2, C₂ 0(두 Cl 교환), σᵥ(xz) 0(교환), σᵥ′(yz) 2(분자 평면)
3. 축소 ($h = 4$):

$$\begin{aligned}
n(A_1) &= \tfrac14[2 + 0 + 0 + 2] = 1, & n(A_2) &= \tfrac14[2 + 0 - 0 - 2] = 0\\
n(B_1) &= \tfrac14[2 - 0 + 0 - 2] = 0, & n(B_2) &= \tfrac14[2 - 0 - 0 + 2] = 1
\end{aligned}$$

$\Gamma = A_1(z) + B_2(y)$ → **둘 다 IR 활성 → 띠 2개**

**단계별 풀이 — trans 이성질체 (D₂ₕ)**

1. trans: 두 Cl이 180°(z축 위), 중심 대칭.
2. Γ(Pd–Cl): E 2, C₂(z) 2, C₂(y) 0, C₂(x) 0, i 0, σ(xy) 0, σ(xz) 2, σ(yz) 2
3. 축소 ($h = 8$):

$$n(A_g) = \tfrac18[2 + 2 + 0 + 0 + 0 + 0 + 2 + 2] = 1,\quad n(B_{1u}) = \tfrac18[2 + 2 - 0 - 0 - 0 - 0 + 2 + 2] = 1$$

나머지 6개는 0 → $\Gamma = A_g + B_{1u}$. IR 활성은 **B₁ᵤ(z)** 하나 → 띠 1개(A_g는 Raman 활성, 상호 배제 원리).

**결론과 진동 방식**

| | X = cis (C₂ᵥ) | Y = trans (D₂ₕ) |
|---|---|---|
| 대칭 신축 | A₁: 두 Pd–Cl이 함께 늘어남 → ν₁ 320 cm⁻¹ | A_g: IR 비활성 |
| 비대칭 신축 | B₂: 하나 늘고 하나 줄어듦 → ν₂ 280 cm⁻¹ | B₁ᵤ: IR 활성 |

IR 띠가 2개 → **X = cis**.

**검산** 대칭 신축이 비대칭보다 높은 파수인 것은 cis 착물의 일반적인 경향과 맞고, 각 표현의 차원 합이 벡터 수(2)와 같습니다.

"""

B['b9'] = r"""
**주어진 것 / 구할 것**

- d⁶, d⁵ Tanabe–Sugano 도표 (스핀 교차: d⁶ Δ/B ≈ 20, d⁵ Δ/B ≈ 28)
- 구할 것: [Fe(CN)₆]⁴⁻ 바닥 항 축퇴도, [Co(NH₃)₆]³⁺ 가장 긴 파장 스핀 허용 띠, [FeF₆]³⁻·[CoF₆]³⁻ 바닥 항과 색 차이의 이유

**풀이 전략** ① 산화수 → dⁿ, ② 리간드 장 세기(분광화학 계열) → 고스핀/저스핀, ③ 도표에서 바닥 항 → ④ 같은 스핀 다중도의 들뜬 항만 스핀 허용.

**단계별 풀이**

1. **[Fe(CN)₆]⁴⁻**: $x + 6(-1) = -4$ → Fe(II), d⁶. CN⁻는 강한 장 → 저스핀 $t_{2g}^6$. 모든 전자가 짝 → S = 0, 꽉 찬 $t_{2g}$ → 궤도 비축퇴 → $^1A_{1g}$. 축퇴도 $= (2S+1)\times(\text{궤도}) = 1\times1 = 1$.
2. **[Co(NH₃)₆]³⁺**: Co(III), d⁶. NH₃와 높은 전하 → 강한 장, 저스핀 $^1A_{1g}$. 스핀 허용(ΔS = 0) 전이는 단일항으로 가는 것뿐: $^1A_{1g}\to{}^1T_{1g}$(낮은 에너지 = **가장 긴 파장**), $^1A_{1g}\to{}^1T_{2g}$. 오비탈로 보면 $t_{2g}^6 \to t_{2g}^5e_g^1$.
3. **[FeF₆]³⁻**: Fe(III), d⁵. F⁻는 약한 장 → 고스핀 $t_{2g}^3e_g^2$, S = 5/2 → $^6A_{1g}$. d⁵ 도표에는 **스핀 다중도 6인 들뜬 항이 없음** → 모든 d–d 전이가 스핀 금지(ΔS ≠ 0) + Laporte 금지 → 흡광 계수 매우 작음 → **무색**(연한 색).
4. **[CoF₆]³⁻**: Co(III), d⁶. F⁻ 약한 장 → 고스핀 $t_{2g}^4e_g^2$, S = 2 → $^5T_{2g}$(축퇴도 5 × 3 = 15). 같은 오중항 들뜬 항 $^5E_g$($t_{2g}^3e_g^3$)가 있어 **스핀 허용 전이 1개** → 가시광 흡수 → **색**.

| 착물 | dⁿ | 스핀 | 배치 | 바닥 항 | 스핀 허용 d–d |
|---|---|---|---|---|---|
| [Fe(CN)₆]⁴⁻ | d⁶ | 저 | $t_{2g}^6$ | $^1A_{1g}$ | ¹T₁g, ¹T₂g |
| [Co(NH₃)₆]³⁺ | d⁶ | 저 | $t_{2g}^6$ | $^1A_{1g}$ | **¹T₁g**(장파장), ¹T₂g |
| [FeF₆]³⁻ | d⁵ | 고 | $t_{2g}^3e_g^2$ | $^6A_{1g}$ | 없음 |
| [CoF₆]³⁻ | d⁶ | 고 | $t_{2g}^4e_g^2$ | $^5T_{2g}$ | $^5E_g$ 1개 |

**검산** 같은 Co(III) d⁶라도 NH₃(강한 장)는 저스핀, F⁻(약한 장)는 고스핀으로 도표의 왼쪽/오른쪽에 놓여 바닥 항이 달라집니다.

"""

B['b10'] = r"""
**주어진 것 / 구할 것**

- A: 4-(3,4-dichlorophenyl)-4-oxobutanoic acid
- (i) NaBH₄ (ii) HCl → B (C₁₀H₈O₂Cl₂) → 벤젠, AlCl₃ → C (C₁₆H₁₄O₂Cl₂) → (1) SOCl₂ (2) AlCl₃ → D (C₁₆H₁₂OCl₂)
- 구할 것: B, C, D 구조와 B → C에서 C가 주생성물인 이유

**풀이 전략** 각 단계의 분자식 변화를 먼저 계산해 무엇이 더해지고 빠지는지 확인한 뒤, 시약의 선택성(NaBH₄: 케톤만, AlCl₃: 양이온 생성)으로 위치를 정합니다.

**단계별 풀이**

1. **분자식 변화 추적**

| 단계 | 분자식 | 변화 | 해석 |
|---|---|---|---|
| A | C₁₀H₈O₃Cl₂ | | 케톤 + COOH |
| A → B | C₁₀H₈O₂Cl₂ | +2H(환원) − H₂O | 케톤 → 알코올 → 분자 내 에스터(락톤) |
| B → C | C₁₆H₁₄O₂Cl₂ | + C₆H₆ | 벤젠이 통째로 붙음(알킬화), 락톤 열림 |
| C → D | C₁₆H₁₂OCl₂ | − H₂O | 분자 내 아실화(고리화) |

2. **A → B.** NaBH₄의 H⁻는 케톤 C=O만 환원(카복실산은 먼저 카복실레이트가 되어 반응 안 함) → γ-하이드록시산. HCl에서 COOH의 C=O가 양성자화 → γ-OH가 분자 내 공격 → 사면체 중간체 → 물 이탈 → **5원 고리 γ-락톤 B**(5원 고리라 분자 내 반응이 빠름).
3. **B → C.** AlCl₃(루이스 산)가 락톤의 **고리(알킬) 산소**에 배위 → 벤질 C–O 결합이 끊어지며 **2차 벤질 탄소양이온** 생성. 양전하가 다이클로로페닐 고리로 공명 비편재화되어 안정 → 벤젠의 π 전자가 이 탄소를 공격(Friedel–Crafts 알킬화) → 아레늄 이온 → H⁺ 제거로 방향족성 회복 → 수용성 후처리로 COOH 회복 → **C**.
4. **C → D.** SOCl₂로 산 염화물 → AlCl₃가 Cl을 떼어 **아실륨 이온** → 분자 내 Friedel–Crafts 아실화. 6원 고리가 생기는 자리이면서 **전자가 더 풍부한 비치환 페닐 고리**의 ortho 탄소가 공격 → 아레늄 이온 → H⁺ 제거 → **D 테트랄론**(4-(3,4-dichlorophenyl)-3,4-dihydronaphthalen-1(2H)-one).

**왜 C가 주생성물인가** AlCl₃가 락톤에서 만들 수 있는 양이온은 두 가지입니다. ① 고리 O–C(벤질) 결합이 끊어진 **벤질 탄소양이온**(아릴 공명 + 2차) ② 카보닐 쪽이 끊어진 아실륨형 양이온. ①이 훨씬 안정하고 쉽게 생기므로 벤젠은 벤질 탄소에 붙고(알킬화), 아실화 생성물(케톤)은 생기지 않습니다. 또 생성물 C에 붙은 새 페닐기는 알킬 치환 벤젠이라 다음 단계 고리화에서 다이클로로페닐(Cl 두 개로 비활성)보다 친전자체를 잘 받아들입니다.

""" + mech('m_B10_nabh4', 'NaBH₄의 케톤 선택적 환원') + mech('m_B10_lactone', 'A → B 락톤 형성') + mech('m_B10_fc', 'B → C Friedel–Crafts 알킬화') + mech('m_B10_acylium', '아실륨 이온 생성과 아레늄 이온 탈양성자화') + mech('m_B10_acyl', 'C → D 분자 내 Friedel–Crafts 아실화') + r"""**검산** 분자식이 모든 단계에서 문제와 일치하고(RDKit 확인), D에 CH₃NH₂(이민) → H₂/Pd-C(환원)를 하면 문제의 sertraline 골격이 됩니다.

"""

B['b11'] = r"""
**주어진 것 / 구할 것**

- 자료 1: pH 6 붕산염 완충액, A⁺, B⁻, 중성 C, 실리카 모세관
- 자료 2: 전기삼투 속도 (E = 4.0 × 10⁴ V/m) — 노출 실리카 pH 10 +3.1, pH 2.5 +0.2 / 아미노프로필 pH 10 +1.8, pH 2.5 −1.3 mm/s
- 자료 3: 양이온 $u_{ep} = u_{eo} = 0.80$ mm/s, 주입구–검출기 40.0 cm
- 구할 것: 이동 시간 순서, pH에 따른 속도 설명, 검출 시간

**풀이 전략** 관측 속도 = 전기삼투 흐름(EOF, 모든 성분이 같은 속도로 음극 쪽) + 각 이온의 전기이동(양이온 음극 쪽 +, 음이온 양극 쪽 −). 벽 표면 전하의 부호와 크기가 EOF를 결정합니다.

**단계별 풀이**

1. **이동 순서** ($u_{net} = u_{eo} + u_{ep}$, 음극 방향 +)
   - A⁺: $u_{eo} + |u_{ep}|$ → 가장 빠름
   - C: $u_{eo}$ → 중간
   - B⁻: $u_{eo} - |u_{ep}|$ → 가장 느림 ($|u_{ep}| < u_{eo}$여야 검출됨)

   이동 시간이 **감소하는 순서: B⁻ > C > A⁺**
2. **벽 전하 → EOF**
   - 노출 실리카: Si–OH ⇌ Si–O⁻ + H⁺ (pKa 약 2~9 분포). pH 10에서는 거의 다 Si–O⁻ → 음전하 큼 → 벽 옆 양이온층이 음극으로 끌려가며 강한 EOF(+3.1). pH 2.5에서는 대부분 Si–OH(중성) → EOF ≈ 0(+0.2).
   - 아미노프로필: –CH₂CH₂CH₂NH₂(pKa ≈ 10). pH 10에서 일부 Si–O⁻는 남지만 일부 표면이 아민으로 덮여 음전하 감소 → EOF 감소(+1.8). pH 2.5에서는 –NH₃⁺로 **벽이 양전하** → 벽 옆에 음이온층이 생겨 양극 쪽으로 흐름 → EOF **방향 역전**(−1.3).
3. **검출 시간**

$$u_{net} = 0.80 + 0.80 = 1.60\ \mathrm{mm/s} = 0.160\ \mathrm{cm/s},\qquad t = \frac{40.0\ \mathrm{cm}}{0.160\ \mathrm{cm/s}} = 250\ \mathrm{s}$$

4. **이동도로 환산(참고)**: $\mu = u/E$ → $\mu_{ep} = \dfrac{0.80\times10^{-3}\ \mathrm{m/s}}{4.0\times10^4\ \mathrm{V/m}} = 2.0\times10^{-8}\ \mathrm{m^2/(V\cdot s)}$ (전형적인 작은 이온 값).

**검산** 중성 C만 있었다면 $40.0/0.080 = 500$ s → 양이온은 전기이동이 더해져 정확히 절반 시간(250 s)에 도착합니다.

"""

def main():
    s = open(MD, encoding='utf-8').read()
    done = []
    for qid, body in B.items():
        i = s.index('{#%s}' % qid)
        j = s.find('\n## ', i + 5)
        j = len(s) if j < 0 else j
        sec = s[i:j]
        if '**주어진 것 / 구할 것**' in sec:
            continue
        a = sec.index('<div class="odds"')
        a = sec.index('</div>', a) + len('</div>')
        b = sec.index('**채점 포인트·함정**')
        sec = sec[:a] + '\n' + body + sec[b:]
        s = s[:i] + sec + s[j:]
        done.append(qid)
    open(MD, 'w', encoding='utf-8').write(s)
    print('expanded', done)

if __name__ == '__main__':
    main()
