#pragma once

#include <vector>
#include <algorithm>

template<typename T>
class ecFrameWork
{
public:
	ecFrameWork(T initValue);

	ecFrameWork(T initValue, T minValue, T maxValue);
	
	virtual ~ecFrameWork() {};

	typedef void (*PFCBR)(T);

	bool Subscribe(PFCBR cbr);

	void SetValue(T newValue);

	T GetValue(void);

private:
	T m_curValue;
	T m_minValue;
	T m_maxValue;
	std::vector<PFCBR> m_cbrTbl;
};

template <typename T>
ecFrameWork<T>::ecFrameWork(T initValue)
{
	m_curValue = initValue;
	m_minValue = initValue;
	m_maxValue = initValue;
}

template <typename T>
ecFrameWork<T>::ecFrameWork(T initValue, T minValue, T maxValue)
{
	m_curValue = initValue;
	m_minValue = minValue;
	m_maxValue = maxValue;
}

template <typename T>
bool ecFrameWork<T>::Subscribe(PFCBR cbr)
{
	if (NULL == cbr)
	{
		return false;
	}

	m_cbrTbl.push_back(cbr);

	return true;
}

template <typename T>
void ecFrameWork<T>::SetValue(T newValue)
{
	if (m_minValue < m_maxValue)
	{
		if ((newValue < m_minValue) || (newValue > m_maxValue))
		{
			std::cout << "value is out of range" << std::endl;
			return;
		}
	}
	else if (m_minValue == m_maxValue)
	{
		/* do nothing */
	}
	else
	{
		return;
	}

	if (newValue != m_curValue)
	{
		m_curValue = newValue;

		for_each(m_cbrTbl.begin(), m_cbrTbl.end(), [&](const PFCBR cbr) {
			cbr(newValue);
		});
	}
}

template <typename T>
T ecFrameWork<T>::GetValue(void)
{
	return m_curValue;
}