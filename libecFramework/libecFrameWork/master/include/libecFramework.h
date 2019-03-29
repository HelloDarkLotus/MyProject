#pragma once

#include <vector>

template<typename T>
class ecFrameWork
{
public:
	ecFrameWork(T initValue) : m_curValue(initValue) {};
	virtual ~ecFrameWork() {};

	void SetValue(T newValue)
	{
		if (m_curValue != newValue)
		{
			m_curValue = newValue;
		}
	}

	T GetValue(void)
	{
		return m_curValue;
	}

private:
	T m_curValue;
	//std::vector<> m_cbrTbl;
};